def calculate_total(price, tax):
    # Branch feature: Apply 10% discount first
    discounted = price * 0.90
    # Branch main: Include 5% service charge on the discounted price plus tax
    return (discounted + tax) * 1.05