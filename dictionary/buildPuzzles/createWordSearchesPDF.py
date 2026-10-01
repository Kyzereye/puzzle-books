from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_as_pdf(grid, filename, title="Word Search Puzzle"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Courier", 12)
    c.drawString(100, 750, title)

    # Draw grid on PDF
    x_offset = 100
    y_offset = 700
    cell_size = 20

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            c.drawString(x_offset + j * cell_size, y_offset - i * cell_size, char)

    c.save()

# Save puzzle and solution as PDFs
save_as_pdf(puzzle, "puzzle.pdf", "Word Search Puzzle")
save_as_pdf(solution, "solution.pdf", "Solution Key")

print("Puzzle saved as 'puzzle.pdf' and solution saved as 'solution.pdf'.")
