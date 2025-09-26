    # Check content type
    content_type = response.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        print(f"✗ Skipped (Not an image): {url}")
        return

    # Generate hash to detect duplicates
    image_hash = md5(response.content).hexdigest()
    if image_hash in downloaded_hashes:
        print(f"✗ Skipped (Duplicate image): {url}")
        return
    downloaded_hashes.add(image_hash)

    # Extract or generate filename
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = f"image_{image_hash[:8]}.jpg"

    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f"✓ Successfully fetched: {filename}")
    print(f"✓ Image saved to {filepath}")

except requests.exceptions.RequestException as e:
    print(f"✗ Connection error for {url}: {e}")
except Exception as e:
    print(f"✗ Unexpected error for {url}: {e}")
