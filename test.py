import streamlit as st

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender should be either 'male' or 'female'")

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level")
    return bmr * activity_multipliers[activity_level]

def calculate_macros(calories, weight, protein_per_kg=1.6, carb_type='mid'):
    protein_grams = protein_per_kg * weight
    protein_calories = protein_grams * 4
    if carb_type == 'high':
        fat_calories = calories * 0.20
    elif carb_type == 'mid':
        fat_calories = calories * 0.25
    elif carb_type == 'low':
        fat_calories = calories * 0.35
    else:
        raise ValueError("Invalid carb type")

    fat_grams = fat_calories / 9
    carbs_calories = calories - (protein_calories + fat_calories)
    carbs_grams = carbs_calories / 4

    return protein_grams, fat_grams, carbs_grams

# Streamlit App
st.title("BMR & TDEE Calculator")

# Input fields
weight = st.number_input("น้ำหนัก (กก.):", min_value=0.0, step=0.1)
height = st.number_input("ส่วนสูง (ซม.):", min_value=0.0, step=0.1)
age = st.number_input("อายุ (ปี):", min_value=0, step=1)
gender = st.selectbox("เพศ:", ["Male", "Female"])
activity_level = st.selectbox("ระดับกิจกรรม:", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
protein_per_kg = st.number_input("โปรตีนต่อกก. (ค่ามาตรฐาน: 1.6):", value=1.6, step=0.1)

if st.button("คำนวณ"):
    try:
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)
        calories_for_loss = tdee - (tdee * 0.20)
        calories_for_gain = tdee + (tdee * 0.20)

        st.write(f"ค่า BMR ของคุณคือ: {bmr:.2f} แคลอรี่/วัน")
        st.write(f"ค่า TDEE ของคุณคือ: {tdee:.2f} แคลอรี่/วัน")

        goals = {
            "รักษาน้ำหนัก": tdee,
            "ลดน้ำหนัก": calories_for_loss,
            "เพิ่มน้ำหนัก": calories_for_gain
        }
        carb_types = ['high', 'mid', 'low']

        for goal_name, calories in goals.items():
            st.write(f"\nสัดส่วนมาโครสำหรับการ{goal_name} ({calories:.2f} แคลอรี่/วัน):")
            for carb_type in carb_types:
                protein, fat, carbs = calculate_macros(calories, weight, protein_per_kg, carb_type)
                st.write(f"- {carb_type.capitalize()} Carb:")
                st.write(f"  โปรตีน: {protein:.2f} กรัม/วัน")
                st.write(f"  ไขมัน: {fat:.2f} กรัม/วัน")
                st.write(f"  คาร์โบไฮเดรต: {carbs:.2f} กรัม/วัน")

    except ValueError as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")