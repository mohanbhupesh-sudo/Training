# Write a Python program to calculate the area and perimeter of a rectangle

def rectangle_area(width, height):
	"""Return area of a rectangle."""
	return width * height


def rectangle_perimeter(width, height):
	"""Return perimeter of a rectangle."""
	return 2 * (width + height)

def main():
	try:
		w = float(input("Enter rectangle width: ").strip())
		h = float(input("Enter rectangle height: ").strip())
	except Exception:
		print("Invalid input")
		return
	area = rectangle_area(w, h)
	peri = rectangle_perimeter(w, h)
	print(f"Area: {area}")
	print(f"Perimeter: {peri}")








if __name__ == "__main__":
	main()
