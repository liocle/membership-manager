# app/pdf/generate_welcome_letter.py

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from models import Member, Membership
from weasyprint import HTML

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=True,
)


def render_letter_html(member: Member, membership: Membership) -> str:
    """
    Render welcome letter as HTML from template.

    Args:
        member (Member): SQLAlchemy Member object
        membership (Membership): Related unpaid Membership

    Returns:
        str: Rendered HTML
    """
    template = env.get_template("welcome_letter.html.jinja2")
    return template.render(member=member, membership=membership)


def generate_pdf(member: Member, membership: Membership, output_dir: Path) -> Path:
    """
    Generate a welcome letter PDF.

    Args:
        member (Member): The member receiving the letter
        membership (Membership): Their unpaid membership
        output_dir (Path): Directory to save PDF in

    Returns:
        Path: Output file path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    html_str = render_letter_html(member, membership)
    filename = f"welcome_letter_{member.reference_number}.pdf"
    output_path = output_dir / filename

    HTML(string=html_str).write_pdf(output_path)
    print(f"✅ PDF created: {output_path}")
    return output_path
