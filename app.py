import streamlit as st
from datetime import datetime
import copy

MANAGER_EMAIL = "manager@gmail.com"
MANAGER_PASSWORD = "manager12345"
REVIEWS_FILE = "reviews.txt"
SALES_FILE = "sales.txt"
LOW_STOCK_LIMIT = 10
CRITICAL_STOCK_LIMIT = 5
MAX_QTY_PER_ITEM = 10 

def now_str():
    """Return current date and time as string."""
    return datetime.now().strftime("%d-%b-%Y %I:%M %p")
def calculate_cart_total(cart):
    """Calculate total price of items in cart."""
    return sum(item["Price"] * item["Quantity"] for item in cart.values())
def add_to_cart(user, name, price, qty):
    """Add item to user's cart."""
    if qty <= 0:
        st.warning("Quantity must be at least 1")
        return
    cart = st.session_state.carts[user]
    if name in cart:
        cart[name]["Quantity"] += qty
    else:
        cart[name] = {"Price": price, "Quantity": qty}
    st.success(f"{qty} x {name} added to cart.")
def load_reviews_from_file():
    """Load reviews from reviews.txt file."""
    reviews = []
    try:
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" | ", 2)
                if len(parts) == 3:
                    t, user, txt = parts
                else:
                    t = now_str()
                    user = "Unknown"
                    txt = line
                reviews.append((t, user, txt))
    except FileNotFoundError:
        pass
    return reviews
def append_review_to_file(time_str, user, txt):
    """Append a new review to reviews.txt file."""
    try:
        with open(REVIEWS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{time_str} | {user} | {txt}\n")
    except Exception as e:
        pass
def save_sale_to_file(user, total, items, time):
    """Append a sale to sales.txt file."""
    try:
        with open(SALES_FILE, "a", encoding="utf-8") as f:
            items_str = ", ".join([f"{n}({i['Quantity']})" for n, i in items.items()])
            f.write(f"{time} | {user} | ₹{total:.2f} | {items_str}\n")
    except Exception as e:
        pass
def get_discount_from_announcement(text):
    if not text:
        return None, 0
    text = text.lower().strip()
    try:
        percent = max(0, min(100, int(text.split("%")[0])))
    except:
        return None, 0
    if "discount on" in text:
        item = text.split("discount on")[1].strip()
        return item, percent
    if "discount" in text:
        words = text.replace("%", "").split()
        for w in words:
            if w not in ["discount", "on"]:
                return w, percent
    return None, 0
open(REVIEWS_FILE, "a").close()
open(SALES_FILE, "a").close()

DEFAULT_INVENTORY = {
    "Vegetables": {
        "Tomato": {"Price": 20.0, "Quantity": 50},
        "Potato": {"Price": 15.0, "Quantity": 40},
        "Onion": {"Price": 25.0, "Quantity": 30},
        "Chilli": {"Price": 50.0, "Quantity": 10},
        "Cabbage": {"Price": 30.0, "Quantity": 20},
        "Carrot": {"Price": 35.0, "Quantity": 25},
        "Cauliflower": {"Price": 40.0, "Quantity": 15},
        "Beetroot": {"Price": 30.0, "Quantity": 18},
        "Spinach": {"Price": 15.0, "Quantity": 22},
        "Capsicum": {"Price": 45.0, "Quantity": 12},
        "Brinjal": {"Price": 28.0, "Quantity": 20},
        "Radish": {"Price": 18.0, "Quantity": 14},
        "Pumpkin": {"Price": 50.0, "Quantity": 10},
        "Bitter Gourd": {"Price": 35.0, "Quantity": 12},
        "Bottle Gourd": {"Price": 25.0, "Quantity": 20},
        "Ladyfinger": {"Price": 22.0, "Quantity": 25},
        "Turnip": {"Price": 20.0, "Quantity": 15},
        "Ridge Gourd": {"Price": 30.0, "Quantity": 10},
        "Fenugreek": {"Price": 12.0, "Quantity": 30},
        "Lettuce": {"Price": 40.0, "Quantity": 8}
    },
    "Fruits": {
        "Apple": {"Price": 100.0, "Quantity": 25},
        "Banana": {"Price": 40.0, "Quantity": 60},
        "Orange": {"Price": 60.0, "Quantity": 30},
        "Mango": {"Price": 120.0, "Quantity": 15},
        "Grapes": {"Price": 80.0, "Quantity": 10},
        "Pineapple": {"Price": 150.0, "Quantity": 12},
        "Papaya": {"Price": 50.0, "Quantity": 20},
        "Watermelon": {"Price": 200.0, "Quantity": 8},
        "Strawberry": {"Price": 300.0, "Quantity": 5},
        "Blueberry": {"Price": 400.0, "Quantity": 3},
        "Guava": {"Price": 60.0, "Quantity": 18},
        "Pomegranate": {"Price": 120.0, "Quantity": 10},
        "Kiwi": {"Price": 250.0, "Quantity": 6},
        "Peach": {"Price": 180.0, "Quantity": 7},
        "Plum": {"Price": 160.0, "Quantity": 9},
        "Cherry": {"Price": 350.0, "Quantity": 4},
        "Lemon": {"Price": 15.0, "Quantity": 30},
        "Coconut": {"Price": 60.0, "Quantity": 12},
        "Apricot": {"Price": 200.0, "Quantity": 5},
        "Jackfruit": {"Price": 250.0, "Quantity": 6}
    }
}

if "inventory" not in st.session_state:
    st.session_state.inventory = copy.deepcopy(DEFAULT_INVENTORY)
if "users" not in st.session_state:
    st.session_state.users = {MANAGER_EMAIL: MANAGER_PASSWORD}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "carts" not in st.session_state:
    st.session_state.carts = {}
if "sales" not in st.session_state:
    st.session_state.sales = []
if "reviews" not in st.session_state:
    st.session_state.reviews = load_reviews_from_file()
if "announcement" not in st.session_state:
    st.session_state.announcement = ""

st.sidebar.image("images (2).png")
st.sidebar.title("Menu")
menu = st.sidebar.radio("Go to", ["Home", "Manager", "Customer"])
if st.session_state.logged_in:
    if st.session_state.current_user == MANAGER_EMAIL and menu != "Manager":
        st.warning("Manager is logged in. Logout to access other tabs.")
        st.stop()
    elif st.session_state.current_user != MANAGER_EMAIL and menu != "Customer":
        st.warning("Customer is logged in. Logout to access other tabs.")
        st.stop()

if menu == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Grocery Store")
        st.subheader("Welcome to our digital grocery store 👋")
        st.caption(f"🕒 {now_str()}")
        st.markdown("---")
        st.subheader("📢 Announcement")
        ann = st.session_state.announcement
        st.info(ann if ann else "No announcements.")
        st.markdown("---")
        veg_count = len(st.session_state.inventory.get("Vegetables", {}))
        fru_count = len(st.session_state.inventory.get("Fruits", {}))
        total_items = veg_count + fru_count
        st.write(f"**Total categories:** {len(st.session_state.inventory.keys())}")
        st.write(f"**Total items:** {total_items}")
    with col2:
        st.image("supermarket.png", width=300)


elif menu == "Manager":
    if not st.session_state.logged_in or st.session_state.current_user != MANAGER_EMAIL:
        st.subheader("Manager Login")
        email = st.text_input("Email", key="mgr_email")
        password = st.text_input("Password", type="password", key="mgr_pwd")
        if st.button("Login", key="mgr_login"):
            if email == MANAGER_EMAIL and password == st.session_state.users.get(MANAGER_EMAIL):
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect manager credentials.")
    else:
        st.header("📊 Manager Dashboard")
        tabs = st.tabs(["Inventory", "Stock Monitor", "Sales Report", "Announcements & Reviews"])

        with tabs[0]:
            st.subheader("Inventory List")
            cat = st.selectbox("Select Category", list(st.session_state.inventory.keys()), key="mgr_cat")
            df = st.session_state.inventory[cat]
            st.dataframe(df, width='stretch')
            action = st.radio("Action", ["Add Item", "Update Item", "Remove Item"], key="mgr_action")
            if action == "Add Item":
                name = st.text_input("Item Name", key="mgr_add_name")
                price = st.number_input("Price", min_value=0.0, format="%.2f", key="mgr_add_price")
                qty = st.number_input("Quantity", min_value=0, step=1, key="mgr_add_qty")
                if st.button("Add Item", key="mgr_add_btn"):
                    if name.strip() == "":
                        st.warning("Item name cannot be empty.")

                    elif price <= 0:
                        st.warning("Price must be greater than 0")

                    elif qty < 0:
                        st.warning("Quantity cannot be negative")

                    else:
                        items = st.session_state.inventory[cat]
                        if any(k.lower() == name.lower() for k in items):
                            st.warning("Item already exists. Use Update instead.")
                        else:
                            items[name] = {"Price": price, "Quantity": int(qty)}
                            st.success(f"{name} added successfully.")
                            st.rerun()

            elif action == "Update Item":
                name = st.text_input("Item Name to Update", key="mgr_upd_name")
                price = st.number_input("New Price", min_value=0.0, format="%.2f", key="mgr_upd_price")
                qty = st.number_input("New Quantity", min_value=0, step=1, key="mgr_upd_qty")
                if st.button("Update Item", key="mgr_upd_btn"):
                    found = next((k for k in st.session_state.inventory[cat] if k.lower() == name.lower()), None)

                    if found:
                        if price <= 0:
                            st.warning("Price must be greater than 0")

                        elif qty < 0:
                            st.warning("Quantity cannot be negative")

                        else:
                            st.session_state.inventory[cat][found] = {
                                "Price": price,
                                "Quantity": int(qty)
                            }
                            st.success(f"{found} updated successfully.")
                            st.rerun()

                    else:
                        st.warning("Item does not exist.")

            elif action == "Remove Item":
                name = st.text_input("Item Name to Remove", key="mgr_rem_name")
                if st.button("Remove Item", key="mgr_rem_btn"):
                    found = next((k for k in st.session_state.inventory[cat] if k.lower() == name.lower()), None)
                    if found:
                        del st.session_state.inventory[cat][found]
                        st.success(f"{found} removed successfully.")
                        st.rerun()
                    else:
                        st.warning("Item does not exist.")

        with tabs[1]:
            st.subheader("Stock Monitoring")
            low_stock = {}
            for cat_name, items in st.session_state.inventory.items():
                for item_name, info in items.items():
                    if info["Quantity"] <= LOW_STOCK_LIMIT:
                        low_stock[f"{cat_name} - {item_name}"] = info
            if low_stock:
                st.dataframe(low_stock, width='stretch')
                for item, info in low_stock.items():
                    if info["Quantity"] <= CRITICAL_STOCK_LIMIT:
                        st.warning(f"⚠️ Critical stock: {item}")
            else:
                st.info("All items have sufficient stock.")

        with tabs[2]:
            st.subheader("Sales Report")
            if st.session_state.sales:
                total_income = sum(s["total"] for s in st.session_state.sales)
                st.write(f"**Total Income:** ₹{total_income:.2f}")
                rows = []
                for s in st.session_state.sales:
                    items_str = ", ".join([f"{n}({i['Quantity']})" for n, i in s["items"].items()])
                    rows.append({"User": s["user"], "Total": s["total"], "Time": s["time"], "Items": items_str})
                st.dataframe(rows, width='stretch')
            else:
                st.info("No sales yet.")

        with tabs[3]:
            st.subheader("Announcements & Reviews")
            st.text_area("Current Announcement", value=st.session_state.announcement, height=100, disabled=True)
            new_ann = st.text_area("Write new announcement")
            if st.button("Update Announcement"):
                if new_ann.strip():
                    if "%" in new_ann and "discount on" not in new_ann.lower():
                        st.warning("⚠️ Discount format should be like: 20% discount on orange")
                    else:
                        st.session_state.announcement = new_ann.strip()
                        st.success("✅ Announcement updated.")
                        st.rerun()
                else:
                    st.warning("Announcement cannot be empty.")
            st.markdown("---")
            st.subheader("Customer Reviews")
            if st.session_state.reviews:
                for t, u, txt in reversed(st.session_state.reviews):
                    st.write(f"**{u}** — {t}")
                    st.write(txt)
                    st.markdown("---")
            else:
                st.info("No reviews yet.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("Logged out.")
            st.rerun()


elif menu == "Customer":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("images (4).png")
    with col2:
        st.header("Customer Section")
        cust_tabs = st.tabs(["Login", "Register", "Browse as Guest"])
        user = st.session_state.current_user if st.session_state.logged_in and st.session_state.current_user != MANAGER_EMAIL else None

    with cust_tabs[0]:
        if not user:
            email = st.text_input("Email", key="cust_email")
            pwd = st.text_input("Password", type="password", key="cust_pwd")
            if st.button("Login", key="cust_login_btn"):
                if email == MANAGER_EMAIL and pwd == st.session_state.users.get(MANAGER_EMAIL):
                    st.error("❌ Invalid credentials.")
                else:
                    if email in st.session_state.users and st.session_state.users[email] == pwd:
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.session_state.carts.setdefault(email, {})
                        st.success(f"Welcome back, {email}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials.")
        else:
            st.info(f"Logged in as {user}. Logout to switch.")

    with cust_tabs[1]:
        if not user:
            reg_email = st.text_input("Enter Email", key="reg_email")
            reg_pass = st.text_input("Enter Password", type="password", key="reg_pass")
            if st.button("Register", key="reg_btn"):
                if reg_email.strip() == "" or reg_pass.strip() == "":
                    st.warning("Email and password cannot be empty.")
                elif reg_email == MANAGER_EMAIL:
                    st.error("❌ This email is reserved and cannot be registered.")
                elif reg_email in st.session_state.users:
                    st.error("❌ Account already exists.")
                else:
                    st.session_state.users[reg_email] = reg_pass
                    st.session_state.logged_in = True
                    st.session_state.current_user = reg_email
                    st.session_state.carts.setdefault(reg_email, {})
                    st.success("✅ Account created! You are now logged in.")
                    st.rerun()
        else:
            st.info(f"Logged in as {user}. Logout to switch.")

    with cust_tabs[2]:
        st.subheader("Browse as Guest")
        st.write("You can view items and read/write reviews here. Login to add to cart or checkout.")
        for cat, items in st.session_state.inventory.items():
            st.write(f"### {cat}")
            for name, info in items.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                col1.write(name)
                col2.write(f"₹{info['Price']:.2f}")
                col3.write(f"{info['Quantity']}")
        st.markdown("---")
        st.subheader("Reviews (view & write)")
        if st.session_state.reviews:
            for t, u, txt in reversed(st.session_state.reviews):
                st.write(f"**{u}** — {t}")
                st.write(txt)
                st.markdown("---")
        else:
            st.info("No reviews yet. Be the first to write one!")
        guest_review = st.text_area("Write a review as Guest", key="guest_review_text")
        if st.button("Submit Review as Guest"):
            if guest_review.strip():
                time_now = now_str()
                st.session_state.reviews.append((time_now, "Guest", guest_review.strip()))
                append_review_to_file(time_now, "Guest", guest_review.strip())
                
                st.success("✅ Review submitted as Guest.")
                st.rerun()
            else:
                st.warning("Please write a review before submitting.")

    if user:
        st.markdown("---")
        st.subheader("Available Products")
        search = st.text_input("🔍 Search items by name")
        category_filter = st.selectbox("Filter category", ["All"] + list(st.session_state.inventory.keys()))
        for cat, items in st.session_state.inventory.items():
            if category_filter != "All" and cat != category_filter:
                continue
            st.write(f"### {cat}")
            for name, info in items.items():
                if search and search.lower() not in name.lower():
                    continue
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                col1.write(name)
                col2.write(f"₹{info['Price']:.2f}")
                col3.write(f"{info['Quantity']}")
                if info["Quantity"] > 0:
                    qty = st.number_input("Qty",min_value=1,max_value=min(MAX_QTY_PER_ITEM, info["Quantity"]),step=1,key=f"qty_{name}")
                    if st.button(f"Add {qty} to Cart", key=f"add_{name}"):
                        if qty <= 0:
                            st.warning("Quantity must be at least 1")
                        elif qty > info["Quantity"]:
                            st.warning(f"Only {info['Quantity']} {name} available in stock")
                        else:
                            add_to_cart(user, name, info["Price"], qty)

                else:
                    col4.write("❌ Out of stock")
        st.markdown("---")
        st.subheader("Your Cart")
        cart = st.session_state.carts.get(user, {})
        if cart:
            total = calculate_cart_total(cart)
            discount_item, discount_percent = get_discount_from_announcement(
                st.session_state.announcement)
            discount = 0
            for item, info in cart.items():
                if discount_item and item.lower() == discount_item.lower():
                    discount = (info["Price"] * info["Quantity"]) * discount_percent / 100

            final_total = total - discount
            if final_total < 0:
                final_total = 0
            if discount > 0:
                st.info(f"Discount: {discount_percent}% on {discount_item.title()}")

            for n, info in cart.items():
                col1, col2 = st.columns([3, 1])
                col1.write(f"{n}: {info['Quantity']} x ₹{info['Price']:.2f} = ₹{info['Price'] * info['Quantity']:.2f}")
                if col2.button("Remove", key=f"remove_{n}"):
                    del cart[n]
                    st.success(f"{n} removed from cart")
                    st.rerun()
            if discount > 0:
                st.success(f"🎉 Discount Applied: -₹{discount:.2f}")

            st.write(f"**Final Total: ₹{final_total:.2f}**")

            if st.button("Checkout"):
                can_checkout = True
                for item_name, inf in cart.items():
                    found = False
                    for cat_items in st.session_state.inventory.values():
                        if item_name in cat_items:
                            if cat_items[item_name]["Quantity"] < inf["Quantity"]:
                                st.warning(f"Not enough stock for {item_name}")
                                can_checkout = False
                            found = True
                    if not found:
                        st.warning(f"{item_name} no longer exists in inventory")
                        can_checkout = False
                if can_checkout:
                    for item_name, inf in cart.items():
                        for cat_items in st.session_state.inventory.values():
                            if item_name in cat_items:
                                cat_items[item_name]["Quantity"] -= inf["Quantity"]
                    time_now = now_str()
                    sale = {"user": user,
                        "total": final_total,
                        "discount": discount,
                        "time": time_now,
                        "items": cart.copy()}
                    st.session_state.sales.append(sale)
                    save_sale_to_file(user, final_total, cart.copy(), time_now)
                    st.session_state.carts[user] = {}
                    st.success("✅ Checkout successful! You can now add a review.")
                    st.rerun()
        else:
            st.info("Cart is empty.")
        st.markdown("---")
        st.subheader("Reviews (view & write)")
        if st.session_state.reviews:
            for t, u, txt in reversed(st.session_state.reviews):
                st.write(f"**{u}** — {t}")
                st.write(txt)
                st.markdown("---")
        else:
            st.info("No reviews yet. Be the first to write one!")
        review_text = st.text_area("Write your review", key="cust_review_text")
        if st.button("Submit Review"):
            if review_text.strip():
                time_now = now_str()
                st.session_state.reviews.append((time_now, user, review_text.strip()))
                append_review_to_file(time_now, user, review_text.strip())
                st.success("✅ Review submitted!")
                st.rerun()
            else:
                st.warning("Please write a review before submitting.")
        st.markdown("---")
        st.subheader("Your Past Bills")
        bills = [s for s in st.session_state.sales if s["user"] == user]
        if bills:
            for i, s in enumerate(reversed(bills), 1):
                st.write(f"**Bill {i} | Time: {s['time']} | Total: ₹{s['total']:.2f}**")
                for n, info in s["items"].items():
                    st.write(f"- {n}: {info['Quantity']} x ₹{info['Price']:.2f}")
                bill_text = f"Bill {i} | Time: {s['time']} | Total: ₹{s['total']:.2f}\n"
                for n, info in s["items"].items():
                    bill_text += f"{n}: {info['Quantity']} x ₹{info['Price']:.2f}\n"
                st.download_button(f"Download Bill {i}", data=bill_text, file_name=f"bill_{i}.txt", mime="text/plain")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("Logged out.")
            st.rerun()
