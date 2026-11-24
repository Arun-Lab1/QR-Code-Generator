import os
import time
from fpdf import FPDF
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import qrcode


class QRGeneratorScreen(BoxLayout):
  current_qr_path = "temp_qr.png"
  current_url = ""

  def generate_qr(self):
    url = self.ids.url_input.text.strip()

    if not url:
      print("Please enter a URL first!")
      return

    self.current_url = url

    # Generate and save the QR code as a temporary image file
    img = qrcode.make(url)
    img.save(self.current_qr_path)

    # Display the image in the app
    self.ids.qr_image.source = self.current_qr_path
    self.ids.qr_image.reload()
    print(f"QR Code generated for: {url}")

  def save_as_pdf(self):
    if not os.path.exists(self.current_qr_path):
      print("Please generate a QR code first!")
      return

    # Find the user's Downloads folder automatically
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = f"QRCode_{int(time.time())}.pdf"
    pdf_path = os.path.join(downloads_folder, filename)

    # Create the PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 15, text="Scan QR Code", new_x="LMARGIN", new_y="NEXT", align="C")

    # Place the QR code image centered on the page
    pdf.image(self.current_qr_path, x=65, y=40, w=80)

    # Print the URL text underneath the QR code
    pdf.set_y(130)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 10, text=self.current_url, align="C")

    # Save the PDF file
    pdf.output(pdf_path)
    print(f"PDF successfully saved to your Downloads folder: {filename}")


class QRApp(App):

  def build(self):
    return QRGeneratorScreen()


if __name__ == "__main__":
  QRApp().run()


# Create by: Arun