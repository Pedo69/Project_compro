import struct, os, re

# ================= File Names =================
FILE_BASIC = "cars_basic.dat"
FILE_STATUS = "cars_status.dat"
FILE_SALE = "cars_sale.dat"

# =============================================

# ================= Structs =================

# 1. Basic: เก็บข้อมูลพื้นฐานของรถแต่ละคันใน cars_basic.dat
#    - car_id (int)         : รหัสรถ (ใช้เป็น key เชื่อมโยงทุกไฟล์)
#    - year (int)           : ปีที่ผลิต
#    - brand (20s)          : ยี่ห้อรถ (string 20 bytes)
#    - model (20s)          : รุ่นรถ (string 20 bytes)
#    - odometer (int)       : เลขไมล์
#    - buy_price (int)      : ราคาซื้อ
struct_basic = struct.Struct("<i i 20s 20s i i")

# 2. Status: เก็บสถานะของรถแต่ละคันใน cars_status.dat
#    - car_id (int)         : รหัสรถ (key เชื่อมโยงกับ cars_basic.dat)
#    - active (int)         : สถานะการใช้งาน (1=active, 0=inactive)
#    - is_sold (int)        : ขายแล้วหรือยัง (1=ขายแล้ว, 0=ยังไม่ขาย)
#    - sell_price (float)   : ราคาขายที่ตั้งไว้
struct_status = struct.Struct("<i i i f")

# 3. Sale: เก็บข้อมูลการขายใน cars_sale.dat
#    - car_id (int)         : รหัสรถ (key เชื่อมโยงกับทุกไฟล์)
#    - buy_price (float)    : ราคาซื้อ (ซ้ำกับ basic เพื่อความสะดวก)
#    - sell_price (float)   : ราคาขายที่ตั้งไว้ (ซ้ำกับ status)
#    - final_price (float)  : ราคาขายจริง (ถ้าขายแล้ว)
#    - customer_name (30s)  : ชื่อลูกค้า (string 30 bytes)
#    - customer_phone (15s) : เบอร์โทรลูกค้า (string 15 bytes)
struct_sale = struct.Struct("<i f f f 30s 15s")

# ================= Helper =================
def encode_str(s, size): 
    return s.encode("utf-8")[:size].ljust(size, b'\x00')

def decode_str(b): 
    return b.split(b'\x00',1)[0].decode("utf-8")

# ================= Save & Load =================

# ...existing code...

def save_all(cars):
    with open(FILE_BASIC, "wb") as fb, open(FILE_STATUS, "wb") as fs, open(FILE_SALE, "wb") as fsl:
        for c in cars:
            car_id_int = int(c["car_id"][1:])  # remove 'C' → int
            # BASIC
            fb.write(struct_basic.pack(
                car_id_int,
                int(c["year"]),
                encode_str(c["brand"], 20),
                encode_str(c["model"], 20),
                int(c["odometer"]),
                int(c["buy_price"])
            ))
            # STATUS
            fs.write(struct_status.pack(
                car_id_int,
                1,  # active
                1 if c["status"].lower() == "yes" else 0,
                float(c["sell_price"])
            ))
            # SALE
            fsl.write(struct_sale.pack(
                car_id_int,
                float(c["buy_price"]),
                float(c["sell_price"]),
                float(c["final_price"]),
                encode_str(c["customer_name"], 30),
                encode_str(c["customer_phone"], 15)
            ))

# ...existing code...


def load_all():
    cars = []
    if not (os.path.exists(FILE_BASIC) and os.path.exists(FILE_STATUS) and os.path.exists(FILE_SALE)):
        return []
    with open(FILE_BASIC,"rb") as fb, open(FILE_STATUS,"rb") as fs, open(FILE_SALE,"rb") as fsl:
        while True:
            cb = fb.read(struct_basic.size)
            cs = fs.read(struct_status.size)
            cl = fsl.read(struct_sale.size)
            if not cb or not cs or not cl:
                break
            b = struct_basic.unpack(cb)
            s = struct_status.unpack(cs)
            l = struct_sale.unpack(cl)
            car_id = f"C{b[0]:03d}"
            cars.append({
                "car_id": car_id,
                "year": b[1],
                "brand": decode_str(b[2]),
                "model": decode_str(b[3]),
                "odometer": b[4],
                "buy_price": b[5],
                "status": "Yes" if s[2] == 1 else "No",
                "sell_price": s[3],
                "final_price": l[3],
                "profit": l[3] - b[5] if l[3] > 0 else 0,
                "customer_name": decode_str(l[4]),
                "customer_phone": decode_str(l[5])
            })
    return cars

# ================= Add =================

# ...existing code...

def Add():
    try:
        cars = load_all()
        # --- Car ID ---
        while True:
            car_id = input("Enter CarID (C001): ").strip().upper()
            if any(c["car_id"] == car_id for c in cars):
                print("Error: CarID already exists!")
                continue
            if not re.fullmatch(r"C\d{3}", car_id):
                print("Error: Format must be Cxxx (e.g., C001)!")
                continue
            break
        # --- Brand ---
        while True:
            brand = input("Brand: ").strip()
            if brand == "":
                print("Error: Brand cannot be empty!")
                continue
            break
        # --- Model ---
        while True:
            model = input("Model: ").strip()
            if model == "":
                print("Error: Model cannot be empty!")
                continue
            break
        # --- Year ---
        while True:
            year_inp = input("Year (YYYY): ").strip()
            if not year_inp.isdigit():
                print("Error: Year must be numbers only!")
                continue
            year = int(year_inp)
            if year < 1900 or year > 2100:
                print("Error: Year out of range!")
                continue
            break
        # --- Odometer ---
        while True:
            odo = input("Odometer (km): ").strip()
            if not odo.isdigit():
                print("Error: Odometer must be numbers only!")
                continue
            odometer = int(odo)
            break
        # --- Buy Price ---
        while True:
            try:
                buy_price = float(input("Buy Price: "))
                if buy_price < 0:
                    print("Error: Buy Price cannot be negative!")
                    continue
                break
            except ValueError:
                print("Error: Buy Price must be a number!")
        # --- Sell Price ---
        while True:
            try:
                sell_price = float(input("Sell Price: "))
                if sell_price < 0:
                    print("Error: Sell Price cannot be negative!")
                    continue
                break
            except ValueError:
                print("Error: Sell Price must be a number!")
        # --- Status ---
        while True:
            status_inp = input("Sold? (Yes/No): ").strip().lower()
            if status_inp not in ["yes", "no"]:
                print("Error: Please enter Yes or No!")
                continue
            break
        # --- Final Price & Customer Info ---
        if status_inp == "yes":
            while True:
                try:
                    final_price = float(input("Final Price: "))
                    if final_price < 0:
                        print("Error: Final Price cannot be negative!")
                        continue
                    break
                except ValueError:
                    print("Error: Final Price must be a number!")
            cname = input("Customer Name: ").strip()
            cphone = input("Customer Phone: ").strip()
        else:
            final_price = 0.0
            cname, cphone = "", ""
        # --- Create Car Dict ---
        car = {
            "car_id": car_id,
            "brand": brand,
            "model": model,
            "year": year,
            "odometer": odometer,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "status": status_inp.capitalize(),
            "final_price": final_price,
            "profit": final_price - buy_price if final_price > 0 else 0,
            "customer_name": cname,
            "customer_phone": cphone
        }
        cars.append(car)
        save_all(cars)
        print("Car added successfully!")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ...existing code...

# ================= Delete =================
# ...existing code...

def Delete():
    cars = load_all()
    car_id = input("Enter CarID to delete: ").strip().upper()
    new_cars = [c for c in cars if c["car_id"] != car_id]
    if len(new_cars) < len(cars):
        save_all(new_cars)
        print("Deleted successfully.")
    else:
        print("Car not found.")

# ...existing code...

import struct, os, re

# ================= File Names =================
FILE_BASIC = "cars_basic.dat"
FILE_STATUS = "cars_status.dat"
FILE_SALE = "cars_sale.dat"

# ================= Structs =================
struct_basic = struct.Struct("<i i 20s 20s i i")
struct_status = struct.Struct("<i i i f")
struct_sale = struct.Struct("<i f f f 30s 15s")

# ================= Helper =================
def encode_str(s, size): 
    return s.encode("utf-8")[:size].ljust(size, b'\x00')

def decode_str(b): 
    return b.split(b'\x00',1)[0].decode("utf-8")

# ================= Save & Load =================
def save_all(cars):
    with open(FILE_BASIC, "wb") as fb, open(FILE_STATUS, "wb") as fs, open(FILE_SALE, "wb") as fsl:
        for c in cars:
            car_id_int = int(c["car_id"][1:])  # remove 'C' → int
            # BASIC
            fb.write(struct_basic.pack(
                car_id_int,
                int(c["year"]),
                encode_str(c["brand"], 20),
                encode_str(c["model"], 20),
                int(c["odometer"]),
                int(c["buy_price"])
            ))
            # STATUS
            fs.write(struct_status.pack(
                car_id_int,
                1,  # active
                1 if c["status"].lower() == "yes" else 0,
                float(c["sell_price"])
            ))
            # SALE
            fsl.write(struct_sale.pack(
                car_id_int,
                float(c["buy_price"]),
                float(c["sell_price"]),
                float(c["final_price"]),
                encode_str(c["customer_name"], 30),
                encode_str(c["customer_phone"], 15)
            ))

def load_all():
    cars = []
    if not (os.path.exists(FILE_BASIC) and os.path.exists(FILE_STATUS) and os.path.exists(FILE_SALE)):
        return []
    with open(FILE_BASIC,"rb") as fb, open(FILE_STATUS,"rb") as fs, open(FILE_SALE,"rb") as fsl:
        while True:
            cb = fb.read(struct_basic.size)
            cs = fs.read(struct_status.size)
            cl = fsl.read(struct_sale.size)
            if not cb or not cs or not cl:
                break
            b = struct_basic.unpack(cb)
            s = struct_status.unpack(cs)
            l = struct_sale.unpack(cl)
            car_id = f"C{b[0]:03d}"
            cars.append({
                "car_id": car_id,
                "year": b[1],
                "brand": decode_str(b[2]),
                "model": decode_str(b[3]),
                "odometer": b[4],
                "buy_price": b[5],
                "status": "Yes" if s[2] == 1 else "No",
                "sell_price": s[3],
                "final_price": l[3],
                "profit": l[3] - b[5] if l[3] > 0 else 0,
                "customer_name": decode_str(l[4]),
                "customer_phone": decode_str(l[5])
            })
    return cars

# ================= Add =================
def Add():
    try:
        cars = load_all()
        # --- Car ID ---
        while True:
            car_id = input("Enter CarID (C001): ").strip().upper()
            if any(c["car_id"] == car_id for c in cars):
                print("Error: CarID already exists!")
                continue
            if not re.fullmatch(r"C\d{3}", car_id):
                print("Error: Format must be Cxxx (e.g., C001)!")
                continue
            break
        # --- Brand ---
        while True:
            brand = input("Brand: ").strip()
            if brand == "":
                print("Error: Brand cannot be empty!")
                continue
            break
        # --- Model ---
        while True:
            model = input("Model: ").strip()
            if model == "":
                print("Error: Model cannot be empty!")
                continue
            break
        # --- Year ---
        while True:
            year_inp = input("Year (YYYY): ").strip()
            if not year_inp.isdigit():
                print("Error: Year must be numbers only!")
                continue
            year = int(year_inp)
            if year < 1900 or year > 2100:
                print("Error: Year out of range!")
                continue
            break
        # --- Odometer ---
        while True:
            odo = input("Odometer (km): ").strip()
            if not odo.isdigit():
                print("Error: Odometer must be numbers only!")
                continue
            odometer = int(odo)
            break
        # --- Buy Price ---
        while True:
            try:
                buy_price = float(input("Buy Price: "))
                if buy_price < 0:
                    print("Error: Buy Price cannot be negative!")
                    continue
                break
            except ValueError:
                print("Error: Buy Price must be a number!")
        # --- Sell Price ---
        while True:
            try:
                sell_price = float(input("Sell Price: "))
                if sell_price < 0:
                    print("Error: Sell Price cannot be negative!")
                    continue
                break
            except ValueError:
                print("Error: Sell Price must be a number!")
        # --- Status ---
        while True:
            status_inp = input("Sold? (Yes/No): ").strip().lower()
            if status_inp not in ["yes", "no"]:
                print("Error: Please enter Yes or No!")
                continue
            break
        # --- Final Price & Customer Info ---
        if status_inp == "yes":
            while True:
                try:
                    final_price = float(input("Final Price: "))
                    if final_price < 0:
                        print("Error: Final Price cannot be negative!")
                        continue
                    break
                except ValueError:
                    print("Error: Final Price must be a number!")
            cname = input("Customer Name: ").strip()
            cphone = input("Customer Phone: ").strip()
        else:
            final_price = 0.0
            cname, cphone = "", ""
        # --- Create Car Dict ---
        car = {
            "car_id": car_id,
            "brand": brand,
            "model": model,
            "year": year,
            "odometer": odometer,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "status": status_inp.capitalize(),
            "final_price": final_price,
            "profit": final_price - buy_price if final_price > 0 else 0,
            "customer_name": cname,
            "customer_phone": cphone
        }
        cars.append(car)
        save_all(cars)
        print("Car added successfully!")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ================= Update =================
def Update():
    try:
        cars = load_all()
        car_id = input("Enter CarID to update: ").strip().upper()
        found = False
        for car in cars:
            if car["car_id"] == car_id:
                found = True
                print(f"Updating {car_id}...")
                if car["status"].lower() == "no":
                    print("Currently not sold → mark SOLD")
                    car["status"] = "Yes"
                    while True:
                        try:
                            final_price = float(input("Final Price: "))
                            if final_price < 0:
                                print("Error: Final Price cannot be negative!")
                                continue
                            car["final_price"] = final_price
                            break
                        except ValueError:
                            print("Error: Final Price must be a number!")
                    while True:
                        cname = input("Customer Name: ").strip()
                        if cname == "":
                            print("Error: Customer Name cannot be empty!")
                            continue
                        car["customer_name"] = cname
                        break
                    while True:
                        cphone = input("Customer Phone: ").strip()
                        if not cphone.isdigit():
                            print("Error: Phone must contain digits only!")
                            continue
                        if len(cphone) < 8 or len(cphone) > 15:
                            print("Error: Phone length must be 8–15 digits!")
                            continue
                        car["customer_phone"] = cphone
                        break
                else:
                    print("Already sold → update details")
                    new_price = input("New Final Price (blank=keep): ").strip()
                    if new_price:
                        try:
                            final_price = float(new_price)
                            if final_price < 0:
                                print("Error: Final Price cannot be negative!.")
                            else:
                                car["final_price"] = final_price
                        except ValueError:
                            print("Error: Invalid number!.")
                    new_name = input("New Customer Name (blank=keep): ").strip()
                    if new_name:
                        car["customer_name"] = new_name
                    new_phone = input("New Customer Phone (blank=keep): ").strip()
                    if new_phone:
                        if new_phone.isdigit() and 8 <= len(new_phone) <= 15:
                            car["customer_phone"] = new_phone
                        else:
                            print("Error: Invalid phone number!.")
                car["profit"] = car["final_price"] - car["buy_price"]
                break
        if not found:
            print("CarID not found!")
            return
        save_all(cars)
        print("Car updated successfully!")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ================= Delete =================
def Delete():
    cars = load_all()
    car_id = input("Enter CarID to delete: ").strip().upper()
    new_cars = [c for c in cars if c["car_id"] != car_id]
    if len(new_cars) < len(cars):
        save_all(new_cars)
        print("Deleted successfully.")
    else:
        print("Car not found.")

# ================= View =================
def View(n:int):
    cars = load_all()
    if not cars:
        print("No cars data.")
        return
    if n == 1:
        cid = input("Enter CarID: ").strip().upper()
        for c in cars:
            if c["car_id"] == cid:
                print("="*80)
                print(f"CarID : {c['car_id']}")
                print(f"Brand : {c['brand']}")
                print(f"Model : {c['model']}")
                print(f"Year  : {c['year']}")
                print(f"Odometer : {c['odometer']:,} km")
                print(f"Buy Price : {c['buy_price']:,}")
                print(f"Sell Price: {c['sell_price']:,}")
                print(f"Status    : {c['status']}")
                print(f"Final Price: {c['final_price']:,}")
                print(f"Profit     : {c['profit']:,}")
                print(f"Customer   : {c['customer_name']} ({c['customer_phone']})")
                print("="*80)
                return
        print("Not found")
    elif n == 2:
        print("="*20, "All Cars", "="*20)
        print(f"{'CarID':<6} | {'Brand':<10} | {'Model':<10} | {'Year':<6} | {'Status'}")
        print("-"*50)
        for c in cars:
            print(f"{c['car_id']:<6} | {c['brand']:<10} | {c['model']:<10} | {c['year']:<6} | {c['status']}")
        print("="*50)
    elif n == 3:
        print("===================================")
        print("Filter Options:")
        print("  1. Brand")
        print("  2. Model")
        print("  3. Year")
        print("  4. Status (Yes/No)")
        choice = input("Enter choice: ").strip()
        filtered = []
        title = ""
        if choice == "1":
            brands = sorted(set(c['brand'] for c in cars))
            print("\nAvailable Brand options:", ", ".join(brands))
            print("-"*50)
            brand = input("Enter Brand: ").strip().lower()
            filtered = [c for c in cars if c['brand'].lower() == brand]
            title = f"Cars Filtered by Brand = {brand.capitalize()}"
        elif choice == "2":
            models = sorted(set(c['model'] for c in cars))
            print("\nAvailable Model options:", ", ".join(models))
            print("-"*50)
            model = input("Enter Model: ").strip().lower()
            filtered = [c for c in cars if c['model'].lower() == model]
            title = f"Cars Filtered by Model = {model.capitalize()}"
        elif choice == "3":
            years = sorted(set(str(c['year']) for c in cars))
            print("\nAvailable Year options:", ", ".join(years))
            print("-"*50)
            year = input("Enter Year (YYYY): ").strip()
            filtered = [c for c in cars if str(c['year']) == year]
            title = f"Cars Filtered by Year = {year}"
        elif choice == "4":
            print("\nAvailable Status options: Yes, No")
            print("-"*50)
            status = input("Enter Status (Yes/No): ").strip().lower()
            filtered = [c for c in cars if c['status'].lower() == status]
            title = f"Cars Filtered by Status = {status.capitalize()}"
        else:
            print("Invalid option!")
            return
        if filtered:
            print(f"\n========= {title} =========")
            print(f"{'CarID':<6} | {'Brand':<10} | {'Model':<10} | {'Year':<6} | {'Status'}")
            print("-"*50)
            for c in filtered:
                print(f"{c['car_id']:<6} | {c['brand']:<10} | {c['model']:<10} | {c['year']:<6} | {c['status']}")
            print("="*50)
        else:
            print("No cars found with this filter.")
    elif n == 4:
        notsold = [c for c in cars if c['status'].lower() == "no"]
        if not notsold:
            print("No unsold cars.")
            return
        print(make_table_not_sold(notsold, "Report: Car Not Sale"))
        print(make_summary(cars, "Overall Summary"))
        report = make_table_not_sold(notsold, "Report: Car Not Sale")
        report += "\n" + make_summary(cars, "Overall Summary")
        with open("report_not_sale.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("report_not_sale.txt generated.")
    elif n == 5:
        sold = [c for c in cars if c['status'].lower() == "yes"]
        if not sold:
            print("No sold cars.")
            return
        print(make_table_sold(sold, "Report: Car Sold with Customer"))
        print(make_summary(cars, "Sold Car Summary"))
        report = make_table_sold(sold, "Report: Car Sold with Customer")
        report += "\n" + make_summary(cars, "Sold Car Summary")
        with open("report_sold.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("report_sold.txt generated.")

# หมายเหตุ: ต้องมีฟังก์ชัน make_table_not_sold, make_table_sold, make_summary ในไฟล์นี้ด้วย

# ---------- Reports ----------
def make_table_not_sold(cars, title):
    line = "+" + "-"*8 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*8 + "+" + "-"*16 + "+" + "-"*15 + "+" + "-"*15 + "+" + "-"*7 + "+"
    header = (
        f"\n{title}\n{line}\n"
        f"| {'CarID':<6} | {'Brand':<10} | {'Model':<10} | {'Year':<6} | {'Odometer(km)':>14} | {'Buy Price':>13} | {'Sell Price':>13} | {'Sold':<5} |\n"
        f"{line}"
    )
    rows = ""
    for car in cars:
        rows += (
            f"\n| {car['car_id']:<6} | {car['brand']:<10} | {car['model']:<10} | {car['year']:<6} | "
            f"{car['odometer']:>14,} | {car['buy_price']:>13,.2f} | {car['sell_price']:>13,.2f} | {car['status']:<5} |"
        )
    return header + rows + f"\n{line}"

def make_table_sold(cars, title):
    line = "+" + "-"*8 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*8 + "+" + "-"*16 + "+" + "-"*15 + "+" + "-"*15 + "+" + "-"*7 + "+" + "-"*15 + "+" + "-"*15 + "+" + "-"*20 + "+" + "-"*17 + "+"
    header = (
        f"\n{title}\n{line}\n"
        f"| {'CarID':<6} | {'Brand':<10} | {'Model':<10} | {'Year':<6} | {'Odometer(km)':>14} | {'Buy Price':>13} | {'Sell Price':>13} | {'Sold':<5} | {'Final Price':>13} | {'Profit':>13} | {'Customer Name':<18} | {'Customer Phone':<15} |\n"
        f"{line}"
    )
    rows = ""
    for car in cars:
        rows += (
            f"\n| {car['car_id']:<6} | {car['brand']:<10} | {car['model']:<10} | {car['year']:<6} | "
            f"{car['odometer']:>14,} | {car['buy_price']:>13,.2f} | {car['sell_price']:>13,.2f} | {car['status']:<5} | "
            f"{car['final_price']:>13,.2f} | {car['profit']:>13,.2f} | {car['customer_name']:<18} | {car['customer_phone']:<15} |"
        )
    return header + rows + f"\n{line}"

def make_summary(cars, title="Summary"):
    total = len(cars)
    sold = len([c for c in cars if c["status"].lower() == "yes"])
    available = total - sold
    prices = [c["final_price"] for c in cars if c["final_price"]]
    brands = {}
    for c in cars:
        brands[c["brand"]] = brands.get(c["brand"], 0) + 1
    summary = []
    summary.append(f"\n{title}")
    summary.append(f"* Total Cars : {total}")
    summary.append(f"* Sold Cars  : {sold}")
    summary.append(f"* Available  : {available}\n")
    if prices:
        summary.append("Price Statistics (Final Price, THB)")
        summary.append(f"* Min : {min(prices):,.2f}")
        summary.append(f"* Max : {max(prices):,.2f}")
        summary.append(f"* Avg : {sum(prices)/len(prices):,.2f}\n")
    summary.append("Cars by Brand")
    for brand, count in brands.items():
        summary.append(f"* {brand:<8}: {count}")
    return "\n".join(summary)
