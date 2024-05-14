from flask import Blueprint, g, jsonify, Response
from werkzeug.exceptions import Unauthorized
from app.web.hooks import login_required, handle_file_upload, load_model
from app.web.db.models import Pdf
from app.web.tasks.embeddings import process_document
from app.web import files
from app.web.config import Config

bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")


@bp.route("/", methods=["GET"])
@login_required
def list():
    pdfs = Pdf.where(user_id=g.user.id)

    return Pdf.as_dicts(pdfs)


@bp.route("/", methods=["POST"])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    #res, status_code = files.upload(file_path)
    res = files.upload(file_path, file_id)

    pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)

    process_document.delay(pdf.id)

    return pdf.as_dict()


@bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
@load_model(Pdf)
def show(pdf):
    return jsonify(
        {
            "pdf": pdf.as_dict(),
            "download_url": files.create_download_url(pdf.id),
        }
    )

@bp.route("/<string:pdf_id>/download", methods=["GET"])
def download_file(pdf_id):
    with open(f"{Config.FILE_STORE}/" + pdf_id, 'rb') as store:
        return Response(store.read(), mimetype='application/pdf')
