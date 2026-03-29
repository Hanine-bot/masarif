from __future__ import annotations

from datetime import date

from flask import Blueprint, current_app, flash, redirect, render_template, request, send_file, url_for


main_bp = Blueprint("main", __name__)


def service():
    return current_app.extensions["service"]


def repository():
    return current_app.extensions["repository"]


@main_bp.route("/")
def dashboard():
    search = request.args.get("search", "").strip()
    entry_type = request.args.get("entry_type", "").strip()
    transactions = repository().list_transactions(search=search, entry_type=entry_type)
    summary = repository().transaction_summary()
    return render_template(
        "dashboard.html",
        transactions=transactions,
        summary=summary,
        search=search,
        entry_type=entry_type,
    )


@main_bp.route("/transactions/new", methods=["GET", "POST"])
def create_transaction():
    if request.method == "POST":
        success, transaction, errors = service().create_transaction(request.form.to_dict())
        if success:
            flash("Transaction created successfully.", "success")
            return redirect(url_for("main.dashboard"))
        for error in errors:
            flash(error, "error")
        form_data = transaction.to_record()
    else:
        form_data = {"transaction_date": date.today().isoformat()}

    return render_template(
        "transaction_form.html",
        form_title="New Accounting Entry",
        submit_label="Save Entry",
        form_action=url_for("main.create_transaction"),
        transaction=form_data,
        categories=service().CATEGORIES,
        payment_methods=service().PAYMENT_METHODS,
    )


@main_bp.route("/transactions/<int:transaction_id>/edit", methods=["GET", "POST"])
def edit_transaction(transaction_id: int):
    existing = repository().get_transaction(transaction_id)
    if not existing:
        flash("Transaction not found.", "error")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        success, transaction, errors = service().update_transaction(transaction_id, request.form.to_dict())
        if success:
            flash("Transaction updated successfully.", "success")
            return redirect(url_for("main.dashboard"))
        for error in errors:
            flash(error, "error")
        form_data = transaction.to_record()
    else:
        form_data = existing

    return render_template(
        "transaction_form.html",
        form_title="Edit Accounting Entry",
        submit_label="Update Entry",
        form_action=url_for("main.edit_transaction", transaction_id=transaction_id),
        transaction=form_data,
        categories=service().CATEGORIES,
        payment_methods=service().PAYMENT_METHODS,
    )


@main_bp.route("/transactions/<int:transaction_id>/delete", methods=["POST"])
def delete_transaction(transaction_id: int):
    repository().delete_transaction(transaction_id)
    flash("Transaction deleted successfully.", "success")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/backups", methods=["GET", "POST"])
def backups():
    if request.method == "POST":
        uploaded_file = request.files.get("backup_file")
        if not uploaded_file or not uploaded_file.filename:
            flash("Please select a CSV or JSON file to import.", "error")
            return redirect(url_for("main.backups"))

        imported_count, errors = service().import_transactions(uploaded_file)
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            flash(f"Backup imported successfully with {imported_count} records.", "success")
        return redirect(url_for("main.backups"))

    export_folder = current_app.config["EXPORT_FOLDER"]
    recent_files = sorted(export_folder.glob("*"), key=lambda path: path.stat().st_mtime, reverse=True)[:10]
    return render_template("backups.html", recent_files=recent_files)


@main_bp.route("/exports/<string:export_format>")
def export_transactions(export_format: str):
    try:
        export_path = service().export_transactions(export_format)
    except ValueError:
        flash("Unsupported export format.", "error")
        return redirect(url_for("main.backups"))

    return send_file(export_path, as_attachment=True, download_name=export_path.name)
