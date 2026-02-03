url = input("Enter a full URL: ")

cleaned_url = url.replace("http://", "")

print("Cleaned URL:", cleaned_url)

parts = cleaned_url.split(".")

domain = parts[1]
print("Domain:", domain)

TLD = parts[2]
# TLD_clean = TLD.strip("/")
TLD_clean = TLD.replace("/", "")
print("Top-Level Domain (TLD):", TLD_clean)