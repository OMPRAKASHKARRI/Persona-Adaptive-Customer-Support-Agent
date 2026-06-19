from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

pdf = SimpleDocTemplate("data/password_reset_guide.pdf")

styles = getSampleStyleSheet()

content = [
    Paragraph("Password Reset Guide", styles["Title"]),
    Paragraph("1. Open Login Page", styles["BodyText"]),
    Paragraph("2. Click Forgot Password", styles["BodyText"]),
    Paragraph("3. Enter Registered Email", styles["BodyText"]),
    Paragraph("4. Check Inbox", styles["BodyText"]),
    Paragraph("5. Follow Reset Link", styles["BodyText"]),
    Paragraph("Common Issues:", styles["Heading2"]),
    Paragraph("- Email not received", styles["BodyText"]),
    Paragraph("- Expired reset link", styles["BodyText"]),
    Paragraph("- Spam folder filtering", styles["BodyText"]),
]

pdf.build(content)

print("PDF Created Successfully")