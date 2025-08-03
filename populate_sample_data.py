from database import SessionLocal, engine
import models

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

SAMPLE_OPPORTUNITIES = [
    {
        "title": "Electric Vehicle Charging Network",
        "market_description": "Network of fast-charging stations in urban areas.",
        "tam_estimate": 5000000000,
        "growth_rate": 0.30,
        "consumer_insight": "EV owners struggle to find reliable fast charging options.",
        "hypothesis": "Convenient charging will accelerate EV adoption.",
    },
    {
        "title": "Telemedicine Platform for Rural Areas",
        "market_description": "Video consultation platform tailored for rural patients.",
        "tam_estimate": 3000000000,
        "growth_rate": 0.22,
        "consumer_insight": "Rural communities lack access to specialty care.",
        "hypothesis": "Remote consultations will improve healthcare outcomes.",
    },
    {
        "title": "Subscription Meal Kit for Diabetics",
        "market_description": "Meal kits designed for diabetic dietary needs.",
        "tam_estimate": 800000000,
        "growth_rate": 0.18,
        "consumer_insight": "Diabetics find meal planning time-consuming.",
        "hypothesis": "Ready-to-cook kits simplify diet management.",
    },
    {
        "title": "AI-Powered Legal Research Tool",
        "market_description": "Artificial intelligence tool for quick legal precedent search.",
        "tam_estimate": 1500000000,
        "growth_rate": 0.27,
        "consumer_insight": "Lawyers spend hours on manual case research.",
        "hypothesis": "Automation will reduce research time and costs.",
    },
    {
        "title": "Smart Home Energy Management System",
        "market_description": "IoT system optimizing household energy consumption.",
        "tam_estimate": 4000000000,
        "growth_rate": 0.20,
        "consumer_insight": "Homeowners want lower energy bills without sacrificing comfort.",
        "hypothesis": "Smart automation can reduce energy usage significantly.",
    },
    {
        "title": "Online Tutoring for STEM Subjects",
        "market_description": "Platform connecting students with STEM tutors.",
        "tam_estimate": 1200000000,
        "growth_rate": 0.19,
        "consumer_insight": "Parents seek convenient, quality tutoring options.",
        "hypothesis": "On-demand tutors improve student performance.",
    },
    {
        "title": "Peer-to-Peer Car Sharing Marketplace",
        "market_description": "Service allowing car owners to rent vehicles to neighbors.",
        "tam_estimate": 2200000000,
        "growth_rate": 0.25,
        "consumer_insight": "Many cars sit unused for most of the day.",
        "hypothesis": "Owners will monetize idle cars through sharing.",
    },
    {
        "title": "Sustainable Packaging for E-commerce",
        "market_description": "Eco-friendly packaging solutions for online retailers.",
        "tam_estimate": 3500000000,
        "growth_rate": 0.21,
        "consumer_insight": "Consumers prefer brands with sustainable practices.",
        "hypothesis": "Green packaging will boost customer loyalty.",
    },
    {
        "title": "Fitness App with Personalized Coaching",
        "market_description": "Mobile app offering custom workout plans and coaching.",
        "tam_estimate": 900000000,
        "growth_rate": 0.26,
        "consumer_insight": "Users struggle to stay motivated with generic programs.",
        "hypothesis": "Personalized guidance increases workout adherence.",
    },
    {
        "title": "Virtual Reality Travel Experiences",
        "market_description": "VR platform providing immersive travel adventures.",
        "tam_estimate": 1000000000,
        "growth_rate": 0.24,
        "consumer_insight": "Many cannot travel due to cost or mobility issues.",
        "hypothesis": "Virtual trips satisfy wanderlust affordably.",
    },
    {
        "title": "Language Learning Chatbot",
        "market_description": "Conversational AI for practicing foreign languages.",
        "tam_estimate": 700000000,
        "growth_rate": 0.23,
        "consumer_insight": "Learners need frequent conversation practice.",
        "hypothesis": "Chatbots provide accessible speaking opportunities.",
    },
    {
        "title": "Organic Baby Food Delivery",
        "market_description": "Subscription service delivering organic baby meals.",
        "tam_estimate": 600000000,
        "growth_rate": 0.17,
        "consumer_insight": "Parents worry about additives in store-bought baby food.",
        "hypothesis": "Fresh, organic meals will win trust and convenience.",
    },
    {
        "title": "Remote Worker Wellness Program",
        "market_description": "Corporate wellness packages for remote employees.",
        "tam_estimate": 500000000,
        "growth_rate": 0.29,
        "consumer_insight": "Remote workers often feel isolated and sedentary.",
        "hypothesis": "Wellness initiatives improve morale and productivity.",
    },
    {
        "title": "AI Customer Service Chatbot",
        "market_description": "Automated customer support for common inquiries.",
        "tam_estimate": 2500000000,
        "growth_rate": 0.28,
        "consumer_insight": "Customers expect instant responses from businesses.",
        "hypothesis": "AI chatbots reduce wait times and support costs.",
    },
    {
        "title": "Mental Health Support Platform",
        "market_description": "Online counseling and peer support community.",
        "tam_estimate": 1800000000,
        "growth_rate": 0.31,
        "consumer_insight": "Many individuals lack access to mental health resources.",
        "hypothesis": "Digital tools can bridge gaps in mental health care.",
    },
    {
        "title": "Digital Mortgage Brokerage",
        "market_description": "Online portal simplifying mortgage comparison and approval.",
        "tam_estimate": 4000000000,
        "growth_rate": 0.16,
        "consumer_insight": "Home buyers find mortgage processes confusing and slow.",
        "hypothesis": "Digital workflows speed up approvals and clarity.",
    },
    {
        "title": "Subscription-Based Pet Supplies",
        "market_description": "Recurring delivery of essential pet products.",
        "tam_estimate": 900000000,
        "growth_rate": 0.20,
        "consumer_insight": "Pet owners often forget to restock necessities.",
        "hypothesis": "Scheduled deliveries ensure convenience and loyalty.",
    },
    {
        "title": "Smart Agriculture Drone Services",
        "market_description": "Drones for crop monitoring and spraying.",
        "tam_estimate": 2000000000,
        "growth_rate": 0.32,
        "consumer_insight": "Farmers seek precision tools to optimize yields.",
        "hypothesis": "Aerial data will enable smarter farming decisions.",
    },
    {
        "title": "Second-Hand Luxury Goods Marketplace",
        "market_description": "Verified platform for buying and selling luxury items.",
        "tam_estimate": 1100000000,
        "growth_rate": 0.27,
        "consumer_insight": "Consumers want affordable access to high-end brands.",
        "hypothesis": "Authentication builds trust in resale markets.",
    },
    {
        "title": "Blockchain Supply Chain Tracking",
        "market_description": "Distributed ledger for end-to-end product traceability.",
        "tam_estimate": 3200000000,
        "growth_rate": 0.26,
        "consumer_insight": "Brands need transparency to combat counterfeiting.",
        "hypothesis": "Immutable records enhance supply chain trust.",
    },
    {
        "title": "On-Demand Laundry Service",
        "market_description": "Pickup and delivery laundry application.",
        "tam_estimate": 600000000,
        "growth_rate": 0.18,
        "consumer_insight": "Urban professionals lack time for household chores.",
        "hypothesis": "Convenient services free up valuable time.",
    },
    {
        "title": "EV Battery Recycling Facility",
        "market_description": "Plant for recycling lithium-ion batteries from EVs.",
        "tam_estimate": 2700000000,
        "growth_rate": 0.34,
        "consumer_insight": "Growing EV adoption will create battery disposal issues.",
        "hypothesis": "Recycling mitigates environmental impact and recovers materials.",
    },
    {
        "title": "Cloud Kitchen for Vegan Cuisine",
        "market_description": "Delivery-only kitchen specializing in vegan meals.",
        "tam_estimate": 750000000,
        "growth_rate": 0.22,
        "consumer_insight": "Vegan consumers crave more delivery options.",
        "hypothesis": "Focused menus improve efficiency and satisfaction.",
    },
    {
        "title": "Mobile Payment Solution for Microbusinesses",
        "market_description": "Lightweight POS system for small vendors.",
        "tam_estimate": 1300000000,
        "growth_rate": 0.30,
        "consumer_insight": "Microbusinesses need affordable digital payment tools.",
        "hypothesis": "Simple mobile systems will drive adoption and sales.",
    },
    {
        "title": "Online Marketplace for Local Artisans",
        "market_description": "E-commerce site showcasing handmade goods.",
        "tam_estimate": 500000000,
        "growth_rate": 0.19,
        "consumer_insight": "Artisans struggle to reach wider audiences.",
        "hypothesis": "Centralized marketplace increases visibility and sales.",
    },
    {
        "title": "AI-Driven Sales Lead Scoring",
        "market_description": "Machine learning tool ranking potential sales leads.",
        "tam_estimate": 1600000000,
        "growth_rate": 0.33,
        "consumer_insight": "Sales teams waste time on low-quality leads.",
        "hypothesis": "Predictive scoring improves conversion rates.",
    },
    {
        "title": "Remote Learning Management System",
        "market_description": "Platform for managing virtual classrooms and coursework.",
        "tam_estimate": 2100000000,
        "growth_rate": 0.28,
        "consumer_insight": "Schools require unified tools for online instruction.",
        "hypothesis": "Integrated systems enhance teaching effectiveness.",
    },
    {
        "title": "3D Printing Service for Prototypes",
        "market_description": "On-demand printing of prototype parts for startups.",
        "tam_estimate": 850000000,
        "growth_rate": 0.24,
        "consumer_insight": "Hardware startups need quick access to prototypes.",
        "hypothesis": "Local printing reduces iteration time and costs.",
    },
    {
        "title": "Biodegradable Personal Care Products",
        "market_description": "Line of compostable personal hygiene items.",
        "tam_estimate": 950000000,
        "growth_rate": 0.21,
        "consumer_insight": "Eco-conscious consumers seek plastic-free alternatives.",
        "hypothesis": "Sustainable products will capture growing eco market.",
    },
    {
        "title": "Micro-Mobility Scooter Rentals",
        "market_description": "App-based rental of electric scooters in cities.",
        "tam_estimate": 1400000000,
        "growth_rate": 0.29,
        "consumer_insight": "Commuters need flexible short-distance transport.",
        "hypothesis": "Easy rentals reduce car dependency for short trips.",
    },
]


def populate():
    db = SessionLocal()
    try:
        for opportunity_data in SAMPLE_OPPORTUNITIES:
            opportunity = models.Opportunity(**opportunity_data)
            db.add(opportunity)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    populate()
