import numpy as np
from PIL import Image


def obfuscate_image(img_array, key=None):
    """Obfuscate image by sorting pixels along diagonals (x+y=k) in reverse order.
    Returns obfuscated array and sort orders for reversal."""
    n, m, c = img_array.shape
    ans = np.zeros((n, m, c), dtype=np.uint8)
    diagonal_orders = []

    # Sort along diagonals (x+y = k)
    for k in range(n + m - 1):
        temp = []
        indices = []
        for x in range(max(0, k - m + 1), min(n, k + 1)):
            y = k - x
            if y < m:
                temp.append(img_array[x, y].copy())
                indices.append((x, y))
        if temp:
            temp = np.array(temp)
            order = np.argsort(temp.sum(axis=1))  # Sort by sum of RGB
            diagonal_orders.append((indices, order))
            temp = temp[order]
            # Assign in reverse order
            for i, (x, y) in enumerate(indices):
                ans[x, y] = temp[-(i + 1)]

    return ans, diagonal_orders


def restore_image(obfuscated_array, diagonal_orders):
    """Restore image using stored sort orders from obfuscation."""
    restored = obfuscated_array.copy()

    # Undo diagonal sorting in reverse order
    for indices, order in reversed(diagonal_orders):
        temp = []
        for x, y in indices:
            temp.append(restored[x, y].copy())
        temp = np.array(temp)
        # Reconstruct original pixel order
        original_positions = np.zeros(len(order), dtype=int)
        original_positions[order] = np.arange(len(order))[::-1]  # Undo reverse assignment
        for i, (x, y) in enumerate(indices):
            restored[x, y] = temp[original_positions[i]]



    return restored

# Usage example
if __name__ == "__main__":
    # Load image
    img = np.array(Image.open("image.png").convert("RGB"), dtype=np.uint8)

    # Obfuscate
    obfuscated, orders = obfuscate_image(img)
    Image.fromarray(obfuscated).save("shuffled_image.png", format="PNG")

    # Restore
    restored = restore_image(obfuscated, orders)
    Image.fromarray(restored).save("restored_image.png", format="PNG")

    # Verify
    print("Restoration successful:", np.array_equal(img, restored))