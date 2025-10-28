import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Culinary Course Selector", page_icon="🍳", layout="wide")

def get_db_connection():
    try:
        import psycopg2
        if 'DATABASE_URL' in os.environ:
            return psycopg2.connect(os.environ['DATABASE_URL'])
        else:
            return None
    except:
        return None

def add_favorite(item_type, item_name):
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'db_unavailable_warned' not in st.session_state:
        st.session_state.db_unavailable_warned = False
    
    db_success = False
    if 'DATABASE_URL' in os.environ:
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO favorites (user_id, item_type, item_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    ('default_user', item_type, item_name)
                )
                conn.commit()
                cur.close()
                conn.close()
                db_success = True
            else:
                if not st.session_state.db_unavailable_warned:
                    st.warning("⚠️ Database temporarily unavailable. Favorites will be saved for this session only.")
                    st.session_state.db_unavailable_warned = True
        except Exception as e:
            if not st.session_state.db_unavailable_warned:
                st.warning("⚠️ Database temporarily unavailable. Favorites will be saved for this session only.")
                st.session_state.db_unavailable_warned = True
    
    if (item_type, item_name) not in st.session_state.favorites:
        st.session_state.favorites.append((item_type, item_name))
    return True

def remove_favorite(item_type, item_name):
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'db_unavailable_warned' not in st.session_state:
        st.session_state.db_unavailable_warned = False
    
    if 'DATABASE_URL' in os.environ:
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM favorites WHERE user_id = %s AND item_type = %s AND item_name = %s",
                    ('default_user', item_type, item_name)
                )
                conn.commit()
                cur.close()
                conn.close()
            else:
                if not st.session_state.db_unavailable_warned:
                    st.warning("⚠️ Database temporarily unavailable. Favorites will be saved for this session only.")
                    st.session_state.db_unavailable_warned = True
        except Exception as e:
            if not st.session_state.db_unavailable_warned:
                st.warning("⚠️ Database temporarily unavailable. Favorites will be saved for this session only.")
                st.session_state.db_unavailable_warned = True
    
    if (item_type, item_name) in st.session_state.favorites:
        st.session_state.favorites.remove((item_type, item_name))
    return True

def get_favorites(item_type=None):
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'db_unavailable_warned' not in st.session_state:
        st.session_state.db_unavailable_warned = False
    
    if 'DATABASE_URL' in os.environ:
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT item_type, item_name FROM favorites WHERE user_id = %s",
                    ('default_user',)
                )
                all_results = cur.fetchall()
                cur.close()
                conn.close()
                
                st.session_state.favorites = all_results
                
                if item_type:
                    return [(name,) for t, name in all_results if t == item_type]
                return all_results
            else:
                if not st.session_state.db_unavailable_warned:
                    st.warning("⚠️ Database temporarily unavailable. Showing favorites from this session only.")
                    st.session_state.db_unavailable_warned = True
        except Exception as e:
            if not st.session_state.db_unavailable_warned:
                st.warning("⚠️ Database temporarily unavailable. Showing favorites from this session only.")
                st.session_state.db_unavailable_warned = True
    
    if item_type:
        return [(name,) for t, name in st.session_state.favorites if t == item_type]
    return st.session_state.favorites

def is_favorite(item_type, item_name):
    favorites = get_favorites(item_type)
    return any(fav[0] == item_name for fav in favorites)

courses_data = {
    "Culinary Arts": {
        "description": "Master the fundamentals of cooking techniques, knife skills, and kitchen management. Learn classic and contemporary cooking methods.",
        "icon": "👨‍🍳"
    },
    "Baking and Pastry Arts": {
        "description": "Explore the art and science of baking, from artisan breads to delicate pastries and desserts.",
        "icon": "🥐"
    },
    "International Cuisine": {
        "description": "Journey through global flavors and cooking traditions from Italian, French, Asian, and Latin American cuisines.",
        "icon": "🌍"
    },
    "Gastronomy and Food Science": {
        "description": "Understand the chemistry and biology behind cooking, flavor development, and food preparation techniques.",
        "icon": "🔬"
    },
    "Nutrition and Dietetics": {
        "description": "Learn about nutritional science, meal planning, and creating healthy, balanced culinary experiences.",
        "icon": "🥗"
    },
    "Hospitality and Restaurant Management": {
        "description": "Develop business skills for running successful restaurants, hotels, and food service operations.",
        "icon": "🏨"
    },
    "Food Styling and Photography": {
        "description": "Master the visual presentation of food for media, advertising, and social platforms.",
        "icon": "📸"
    },
    "Culinary Entrepreneurship": {
        "description": "Build your own food business with skills in branding, marketing, finance, and operations management.",
        "icon": "💼"
    },
    "Molecular Gastronomy": {
        "description": "Experiment with modern cooking techniques using scientific principles and innovative presentations.",
        "icon": "⚗️"
    },
    "Beverage and Mixology": {
        "description": "Study the art of crafting cocktails, wine pairing, coffee preparation, and beverage management.",
        "icon": "🍹"
    }
}

colleges_data = {
    "Culinary Arts": [
        {"name": "Le Cordon Bleu", "location": "Paris, France", "country": "France", "tuition": 35000, "duration": "9 months", "rating": 4.8, "accreditation": "French Ministry of Education", "facilities": "Professional kitchens, Wine cellar, Library", "contact": "https://www.cordonbleu.edu/paris", "email": "admissions@cordonbleu.edu"},
        {"name": "Culinary Institute of America", "location": "New York, USA", "country": "USA", "tuition": 32000, "duration": "2 years", "rating": 4.7, "accreditation": "Middle States Commission", "facilities": "45 kitchens, Restaurants, Bakery cafe", "contact": "https://www.ciachef.edu", "email": "admissions@ciachef.edu"},
        {"name": "Institute of Culinary Education", "location": "New York, USA", "country": "USA", "tuition": 28000, "duration": "13 months", "rating": 4.6, "accreditation": "ACCSC", "facilities": "Demo kitchens, Student lounge, Event space", "contact": "https://www.ice.edu", "email": "admissions@ice.edu"},
        {"name": "Johnson & Wales University", "location": "Rhode Island, USA", "country": "USA", "tuition": 25000, "duration": "4 years", "rating": 4.5, "accreditation": "NEASC", "facilities": "Student-run restaurants, Baking labs, Hospitality center", "contact": "https://www.jwu.edu", "email": "admissions@jwu.edu"},
        {"name": "Auguste Escoffier School", "location": "Colorado, USA", "country": "USA", "tuition": 22000, "duration": "1 year", "rating": 4.4, "accreditation": "ACCSC", "facilities": "Farm-to-table program, Production kitchen, Garden", "contact": "https://www.escoffier.edu", "email": "admissions@escoffier.edu"}
    ],
    "Baking and Pastry Arts": [
        {"name": "Le Cordon Bleu Paris", "location": "Paris, France", "country": "France", "tuition": 38000, "duration": "9 months", "rating": 4.9, "accreditation": "French Ministry of Education", "facilities": "Pastry kitchens, Chocolate workshop, Demonstration room", "contact": "https://www.cordonbleu.edu/paris/pastry", "email": "pastry@cordonbleu.edu"},
        {"name": "French Pastry School", "location": "Chicago, USA", "country": "USA", "tuition": 26000, "duration": "16 weeks", "rating": 4.7, "accreditation": "ACCET", "facilities": "European-style kitchens, Artisan bread lab, Sugar work studio", "contact": "https://www.frenchpastryschool.com", "email": "info@frenchpastryschool.com"},
        {"name": "International Culinary Center", "location": "New York, USA", "country": "USA", "tuition": 29000, "duration": "6 months", "rating": 4.6, "accreditation": "ACCSC", "facilities": "Pastry labs, Plated dessert kitchen, Chocolate tempering room", "contact": "https://www.internationalculinarycenter.com", "email": "admissions@icc.edu"},
        {"name": "Culinary Institute of America", "location": "California, USA", "country": "USA", "tuition": 30000, "duration": "2 years", "rating": 4.7, "accreditation": "WASC", "facilities": "Baking & pastry center, Research kitchen, Retail bakery", "contact": "https://www.ciachef.edu/california", "email": "admissions@ciachef.edu"},
        {"name": "Kendall College", "location": "Chicago, USA", "country": "USA", "tuition": 24000, "duration": "1 year", "rating": 4.5, "accreditation": "HLC", "facilities": "Baking labs, Dining room, Student bakery", "contact": "https://www.kendall.edu", "email": "admissions@kendall.edu"}
    ],
    "International Cuisine": [
        {"name": "Westminster Kingsway College", "location": "London, UK", "country": "UK", "tuition": 18000, "duration": "2 years", "rating": 4.6, "accreditation": "Ofsted", "facilities": "Multiple cuisine kitchens, Training restaurant, Wine training", "contact": "https://www.westking.ac.uk", "email": "info@westking.ac.uk"},
        {"name": "Apicius International School", "location": "Florence, Italy", "country": "Italy", "tuition": 20000, "duration": "3 years", "rating": 4.7, "accreditation": "Italian MIUR", "facilities": "Italian cooking lab, Wine cellar, Tuscan villa", "contact": "https://www.apicius.it", "email": "admissions@apicius.it"},
        {"name": "Bangkok Culinary Academy", "location": "Bangkok, Thailand", "country": "Thailand", "tuition": 15000, "duration": "1 year", "rating": 4.5, "accreditation": "Thai Ministry of Education", "facilities": "Thai cuisine kitchen, Street food lab, Spice garden", "contact": "https://www.bangkokcooking.com", "email": "info@bangkokcooking.com"},
        {"name": "Le Cordon Bleu Madrid", "location": "Madrid, Spain", "country": "Spain", "tuition": 28000, "duration": "9 months", "rating": 4.6, "accreditation": "Spanish Ministry of Education", "facilities": "Mediterranean kitchen, Tapas bar, Wine tasting room", "contact": "https://www.cordonbleu.edu/madrid", "email": "madrid@cordonbleu.edu"},
        {"name": "George Brown College", "location": "Toronto, Canada", "country": "Canada", "tuition": 16000, "duration": "2 years", "rating": 4.4, "accreditation": "Ontario College Quality", "facilities": "Global cuisine kitchens, Chef's table, Research center", "contact": "https://www.georgebrown.ca", "email": "admissions@georgebrown.ca"}
    ],
    "Gastronomy and Food Science": [
        {"name": "Basque Culinary Center", "location": "San Sebastian, Spain", "country": "Spain", "tuition": 40000, "duration": "4 years", "rating": 4.9, "accreditation": "Spanish ANECA", "facilities": "Research labs, Innovation kitchen, Gastronomic library", "contact": "https://www.bculinary.com", "email": "info@bculinary.com"},
        {"name": "University of Gastronomic Sciences", "location": "Pollenzo, Italy", "country": "Italy", "tuition": 35000, "duration": "3 years", "rating": 4.8, "accreditation": "Italian MIUR", "facilities": "Food bank, Experimental garden, Wine bank", "contact": "https://www.unisg.it", "email": "admissions@unisg.it"},
        {"name": "Boston University", "location": "Boston, USA", "country": "USA", "tuition": 45000, "duration": "4 years", "rating": 4.7, "accreditation": "NEASC", "facilities": "Science labs, Sensory analysis room, Food innovation center", "contact": "https://www.bu.edu/gastronomy", "email": "gastronomy@bu.edu"},
        {"name": "Copenhagen University", "location": "Copenhagen, Denmark", "country": "Denmark", "tuition": 12000, "duration": "2 years", "rating": 4.6, "accreditation": "Danish Ministry", "facilities": "Food science labs, Nordic food lab, Fermentation facility", "contact": "https://www.ku.dk", "email": "admissions@ku.dk"},
        {"name": "University of Adelaide", "location": "Adelaide, Australia", "country": "Australia", "tuition": 30000, "duration": "3 years", "rating": 4.5, "accreditation": "TEQSA", "facilities": "Wine science center, Food testing lab, Brewery", "contact": "https://www.adelaide.edu.au", "email": "admissions@adelaide.edu.au"}
    ],
    "Nutrition and Dietetics": [
        {"name": "New York University", "location": "New York, USA", "country": "USA", "tuition": 48000, "duration": "4 years", "rating": 4.8, "accreditation": "ACEND", "facilities": "Nutrition clinic, Metabolic kitchen, Research labs", "contact": "https://www.nyu.edu/nutrition", "email": "nutrition.admissions@nyu.edu"},
        {"name": "Cornell University", "location": "New York, USA", "country": "USA", "tuition": 50000, "duration": "4 years", "rating": 4.9, "accreditation": "ACEND", "facilities": "Human metabolic lab, Teaching kitchen, Community clinic", "contact": "https://www.cornell.edu", "email": "admissions@cornell.edu"},
        {"name": "University of Texas", "location": "Austin, USA", "country": "USA", "tuition": 28000, "duration": "4 years", "rating": 4.6, "accreditation": "ACEND", "facilities": "Sports nutrition lab, Clinical practice center, Computer labs", "contact": "https://www.utexas.edu", "email": "admissions@utexas.edu"},
        {"name": "Penn State University", "location": "Pennsylvania, USA", "country": "USA", "tuition": 32000, "duration": "4 years", "rating": 4.7, "accreditation": "ACEND", "facilities": "Dietetic internship center, Food service lab, Counseling rooms", "contact": "https://www.psu.edu", "email": "admissions@psu.edu"},
        {"name": "Kansas State University", "location": "Kansas, USA", "country": "USA", "tuition": 22000, "duration": "4 years", "rating": 4.5, "accreditation": "ACEND", "facilities": "Food science building, Wellness center, Teaching labs", "contact": "https://www.k-state.edu", "email": "admissions@k-state.edu"}
    ],
    "Hospitality and Restaurant Management": [
        {"name": "Swiss Hotel Management School", "location": "Montreux, Switzerland", "country": "Switzerland", "tuition": 45000, "duration": "3 years", "rating": 4.9, "accreditation": "EduQua", "facilities": "On-campus hotel, Conference rooms, Fine dining restaurant", "contact": "https://www.shms.com", "email": "info@shms.com"},
        {"name": "Cornell School of Hotel Administration", "location": "New York, USA", "country": "USA", "tuition": 50000, "duration": "4 years", "rating": 4.9, "accreditation": "ACPHA", "facilities": "Statler Hotel, Beverage center, Hospitality labs", "contact": "https://www.sha.cornell.edu", "email": "sha_admissions@cornell.edu"},
        {"name": "Glion Institute", "location": "Glion, Switzerland", "country": "Switzerland", "tuition": 42000, "duration": "3.5 years", "rating": 4.8, "accreditation": "EduQua", "facilities": "Luxury training hotel, Event spaces, Business center", "contact": "https://www.glion.edu", "email": "info@glion.edu"},
        {"name": "Les Roches", "location": "Crans-Montana, Switzerland", "country": "Switzerland", "tuition": 40000, "duration": "3.5 years", "rating": 4.7, "accreditation": "EduQua", "facilities": "Training hotel, Restaurant, Bar & lounge", "contact": "https://www.lesroches.edu", "email": "info@lesroches.edu"},
        {"name": "Johnson & Wales University", "location": "Rhode Island, USA", "country": "USA", "tuition": 26000, "duration": "4 years", "rating": 4.6, "accreditation": "ACPHA", "facilities": "Hotel operations lab, Event planning center, Dining facilities", "contact": "https://www.jwu.edu/hospitality", "email": "admissions@jwu.edu"}
    ],
    "Food Styling and Photography": [
        {"name": "Institute of Culinary Education", "location": "New York, USA", "country": "USA", "tuition": 18000, "duration": "12 weeks", "rating": 4.7, "accreditation": "ACCSC", "facilities": "Photo studio, Styling kitchen, Prop room", "contact": "https://www.ice.edu/styling", "email": "admissions@ice.edu"},
        {"name": "The Art Institutes", "location": "California, USA", "country": "USA", "tuition": 24000, "duration": "2 years", "rating": 4.5, "accreditation": "WASC", "facilities": "Photography studios, Digital labs, Gallery space", "contact": "https://www.artinstitutes.edu", "email": "admissions@artinstitutes.edu"},
        {"name": "Academy of Art University", "location": "San Francisco, USA", "country": "USA", "tuition": 28000, "duration": "2 years", "rating": 4.6, "accreditation": "WASC", "facilities": "Professional studios, Post-production suite, Exhibition space", "contact": "https://www.academyart.edu", "email": "info@academyart.edu"},
        {"name": "School of Visual Arts", "location": "New York, USA", "country": "USA", "tuition": 35000, "duration": "2 years", "rating": 4.7, "accreditation": "NASAD", "facilities": "State-of-art studios, Equipment rental, Darkrooms", "contact": "https://www.sva.edu", "email": "admissions@sva.edu"},
        {"name": "International Culinary Studio", "location": "Los Angeles, USA", "country": "USA", "tuition": 15000, "duration": "6 months", "rating": 4.4, "accreditation": "BPPE", "facilities": "Commercial kitchen, Lighting studio, Editing suite", "contact": "https://www.icsla.com", "email": "info@icsla.com"}
    ],
    "Culinary Entrepreneurship": [
        {"name": "Culinary Institute of America", "location": "California, USA", "country": "USA", "tuition": 33000, "duration": "2 years", "rating": 4.8, "accreditation": "WASC", "facilities": "Business incubator, Marketing lab, Pop-up restaurant space", "contact": "https://www.ciachef.edu/business", "email": "admissions@ciachef.edu"},
        {"name": "Johnson & Wales University", "location": "Florida, USA", "country": "USA", "tuition": 27000, "duration": "4 years", "rating": 4.6, "accreditation": "SACSCOC", "facilities": "Entrepreneurship center, Food truck, Business simulation lab", "contact": "https://www.jwu.edu/business", "email": "admissions@jwu.edu"},
        {"name": "Drexel University", "location": "Philadelphia, USA", "country": "USA", "tuition": 38000, "duration": "4 years", "rating": 4.7, "accreditation": "MSCHE", "facilities": "Innovation studio, Co-op program, Venture lab", "contact": "https://www.drexel.edu", "email": "admissions@drexel.edu"},
        {"name": "Institute of Culinary Education", "location": "New York, USA", "country": "USA", "tuition": 21000, "duration": "1 year", "rating": 4.5, "accreditation": "ACCSC", "facilities": "Business workshops, Mentorship program, Industry connections", "contact": "https://www.ice.edu/business", "email": "admissions@ice.edu"},
        {"name": "Hult International Business School", "location": "San Francisco, USA", "country": "USA", "tuition": 44000, "duration": "1 year", "rating": 4.7, "accreditation": "AACSB", "facilities": "Startup accelerator, Global campus network, Executive coaching", "contact": "https://www.hult.edu", "email": "admissions@hult.edu"}
    ],
    "Molecular Gastronomy": [
        {"name": "Basque Culinary Center", "location": "San Sebastian, Spain", "country": "Spain", "tuition": 42000, "duration": "1 year", "rating": 4.9, "accreditation": "Spanish ANECA", "facilities": "Molecular gastronomy lab, R&D kitchen, Scientific equipment", "contact": "https://www.bculinary.com/molecular", "email": "info@bculinary.com"},
        {"name": "El Celler de Can Roca", "location": "Girona, Spain", "country": "Spain", "tuition": 25000, "duration": "6 months", "rating": 4.8, "accreditation": "Private institution", "facilities": "3-Michelin star kitchen, Innovation lab, Private mentorship", "contact": "https://www.cellercanroca.com", "email": "info@cellercanroca.com"},
        {"name": "The Fat Duck", "location": "Berkshire, UK", "country": "UK", "tuition": 30000, "duration": "3 months", "rating": 4.9, "accreditation": "Private institution", "facilities": "Experimental kitchen, Sensory lab, Development center", "contact": "https://www.thefatduck.co.uk", "email": "info@thefatduck.co.uk"},
        {"name": "Harvard Science & Cooking", "location": "Cambridge, USA", "country": "USA", "tuition": 8000, "duration": "Online", "rating": 4.6, "accreditation": "Harvard University", "facilities": "Virtual labs, Online resources, Expert lectures", "contact": "https://www.seas.harvard.edu/cooking", "email": "cooking@seas.harvard.edu"},
        {"name": "Alicia Foundation", "location": "Barcelona, Spain", "country": "Spain", "tuition": 20000, "duration": "6 months", "rating": 4.7, "accreditation": "Private foundation", "facilities": "Food science lab, Research library, Test kitchen", "contact": "https://www.fundacionalicia.org", "email": "info@fundacionalicia.org"}
    ],
    "Beverage and Mixology": [
        {"name": "European Bartender School", "location": "Barcelona, Spain", "country": "Spain", "tuition": 12000, "duration": "4 weeks", "rating": 4.7, "accreditation": "IBA certified", "facilities": "Professional bars, Cocktail labs, Flair training area", "contact": "https://www.europeanbartenderschool.com", "email": "info@europeanbartenderschool.com"},
        {"name": "American Bartenders School", "location": "New York, USA", "country": "USA", "tuition": 9000, "duration": "2 weeks", "rating": 4.5, "accreditation": "State licensed", "facilities": "Full service bars, Speed training, Mixology station", "contact": "https://www.barschool.com", "email": "info@barschool.com"},
        {"name": "International Bartender Course", "location": "London, UK", "country": "UK", "tuition": 15000, "duration": "12 weeks", "rating": 4.6, "accreditation": "WSET", "facilities": "Bar training center, Spirit library, Cocktail development lab", "contact": "https://www.barschool.co.uk", "email": "info@barschool.co.uk"},
        {"name": "BarSmarts", "location": "Online/Various", "country": "USA", "tuition": 5000, "duration": "Self-paced", "rating": 4.4, "accreditation": "Industry recognized", "facilities": "Online platform, Virtual tastings, Certification exams", "contact": "https://www.barsmarts.com", "email": "support@barsmarts.com"},
        {"name": "Napa Valley Wine Academy", "location": "California, USA", "country": "USA", "tuition": 18000, "duration": "1 year", "rating": 4.8, "accreditation": "WSET", "facilities": "Wine tasting rooms, Vineyard access, Cellar tours", "contact": "https://www.napavalleywineacademy.com", "email": "info@napavalleywineacademy.com"}
    ]
}

if 'comparing_courses' not in st.session_state:
    st.session_state.comparing_courses = []
if 'show_college_detail' not in st.session_state:
    st.session_state.show_college_detail = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

query_params = st.query_params
if 'course' in query_params:
    st.session_state.selected_course = query_params['course']
elif 'selected_course' not in st.session_state:
    st.session_state.selected_course = None

st.markdown("""
    <style>
    * {
        box-sizing: border-box;
    }
    .main {
        background-color: #FFF8F0;
        padding: 1rem;
        max-width: 100vw;
        overflow-x: hidden;
    }
    .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .course-card {
        background-color: #2D1B4E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(45, 27, 78, 0.3);
        margin: 10px 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
        color: #ffffff;
    }
    .course-card:hover {
        border-color: rgba(139, 92, 246, 0.5);
    }
    .stButton>button {
        background-color: #FF6B35;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        min-height: 44px;
    }
    .stButton>button:hover {
        background-color: #E85A2C;
    }
    .college-detail-box {
        background-color: #1a1a2e;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #8B5CF6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        margin: 15px 0;
        color: #ffffff;
    }
    .comparison-card {
        background-color: #2D1B4E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(45, 27, 78, 0.3);
        margin: 10px 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
        color: #ffffff;
    }
    
    /* Tablet Responsive - 768px and below */
    @media screen and (max-width: 768px) {
        .main {
            padding: 0.5rem !important;
            max-width: 100vw !important;
        }
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        h3 {
            font-size: 1.3rem !important;
        }
        .course-card {
            padding: 15px;
            margin: 8px 0;
            width: 100% !important;
            max-width: 100% !important;
        }
        .college-detail-box {
            padding: 18px;
            margin: 12px 0;
            width: 100% !important;
        }
        .comparison-card {
            padding: 15px;
            margin: 8px 0;
            width: 100% !important;
        }
        .stButton>button {
            padding: 12px 16px;
            font-size: 0.95rem;
        }
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
            width: 100% !important;
        }
        .row-widget {
            width: 100% !important;
        }
        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    /* Mobile Responsive - 480px and below */
    @media screen and (max-width: 480px) {
        .main {
            padding: 0.25rem !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100vw !important;
        }
        h1 {
            font-size: 1.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        h2 {
            font-size: 1.3rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
        .course-card {
            padding: 12px !important;
            margin: 6px 0 !important;
            border-radius: 8px !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        .college-detail-box {
            padding: 15px !important;
            margin: 10px 0 !important;
            border-radius: 10px !important;
            border-left-width: 3px !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        .comparison-card {
            padding: 12px !important;
            margin: 6px 0 !important;
            border-radius: 8px !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        .stButton>button {
            padding: 14px 12px;
            font-size: 0.9rem;
            min-height: 48px;
            width: 100% !important;
        }
        [data-testid="stSidebar"] {
            min-width: 100% !important;
        }
        [data-testid="column"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        .stRadio > div {
            flex-direction: column;
        }
        div[data-baseweb="select"] {
            font-size: 0.9rem;
            width: 100% !important;
        }
        .stSlider {
            padding: 0.5rem 0;
            width: 100% !important;
        }
        .stDataFrame {
            width: 100% !important;
            overflow-x: auto !important;
        }
        .row-widget {
            width: 100% !important;
        }
        .element-container {
            width: 100% !important;
        }
    }
    
    /* Touch-friendly interactions */
    @media (hover: none) and (pointer: coarse) {
        .stButton>button {
            min-height: 48px;
            padding: 14px 20px;
        }
        .course-card {
            margin: 10px 0;
        }
    }
    
    /* Ensure text remains readable on all screens */
    @media screen and (max-width: 768px) {
        p, div, span {
            font-size: 0.95rem;
        }
    }
    
    @media screen and (max-width: 480px) {
        p, div, span {
            font-size: 0.9rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍳 Culinary Course Explorer")
st.markdown("### Discover Your Perfect Culinary Path")
st.markdown("---")

page = st.sidebar.radio("Navigation", ["🏠 Browse Courses", "🎓 View Colleges", "📊 Compare Courses", "❤️ My Favorites"])

if page == "🏠 Browse Courses":
    st.header("Choose Your Culinary Specialty")
    st.write("Select a course to explore colleges offering this program")
    
    cols = st.columns(2)
    
    for idx, (course_name, course_info) in enumerate(courses_data.items()):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="course-card">
                    <h3>{course_info['icon']} {course_name}</h3>
                    <p>{course_info['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([2, 1, 1])
            
            with col_a:
                if st.button(f"View Colleges", key=f"btn_{course_name}"):
                    st.session_state.selected_course = course_name
                    st.query_params['course'] = course_name
                    st.success(f"✅ Selected: {course_name}")
                    st.info("Navigate to 'View Colleges' page!")
            
            with col_b:
                if is_favorite('course', course_name):
                    if st.button("💔 Unfavorite", key=f"unfav_{course_name}"):
                        remove_favorite('course', course_name)
                        st.rerun()
                else:
                    if st.button("❤️ Favorite", key=f"fav_{course_name}"):
                        add_favorite('course', course_name)
                        st.rerun()
            
            with col_c:
                if course_name in st.session_state.comparing_courses:
                    if st.button("➖ Remove", key=f"cmp_rem_{course_name}"):
                        st.session_state.comparing_courses.remove(course_name)
                        st.rerun()
                else:
                    if st.button("➕ Compare", key=f"cmp_add_{course_name}"):
                        if len(st.session_state.comparing_courses) < 3:
                            st.session_state.comparing_courses.append(course_name)
                            st.rerun()
                        else:
                            st.warning("You can compare up to 3 courses at a time")

elif page == "🎓 View Colleges":
    st.header("🎓 Culinary Colleges & Institutes")
    
    if st.session_state.selected_course:
        st.info(f"📚 Showing colleges for: **{st.session_state.selected_course}**")
    else:
        st.warning("⚠️ Please select a course from the 'Browse Courses' page first!")
    
    st.markdown("### Filter Options")
    
    if 'filter_budget_min' not in st.session_state:
        st.session_state.filter_budget_min = int(query_params.get('budget_min', 5000))
    if 'filter_budget_max' not in st.session_state:
        st.session_state.filter_budget_max = int(query_params.get('budget_max', 50000))
    if 'filter_min_rating' not in st.session_state:
        st.session_state.filter_min_rating = float(query_params.get('min_rating', 0.0))
    if 'filter_search' not in st.session_state:
        st.session_state.filter_search = query_params.get('search', '')
    if 'filter_countries' not in st.session_state:
        if 'countries' in query_params:
            country_str = query_params.get('countries', '')
            st.session_state.filter_countries = country_str.split(',') if country_str else []
        else:
            st.session_state.filter_countries = []
    if 'filter_durations' not in st.session_state:
        if 'durations' in query_params:
            duration_str = query_params.get('durations', '')
            st.session_state.filter_durations = duration_str.split(',') if duration_str else []
        else:
            st.session_state.filter_durations = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget_range = st.slider(
            "Annual Tuition Budget (USD)",
            min_value=5000,
            max_value=50000,
            value=(st.session_state.filter_budget_min, st.session_state.filter_budget_max),
            step=1000,
            format="$%d",
            key="budget_slider"
        )
        if budget_range != (st.session_state.filter_budget_min, st.session_state.filter_budget_max):
            st.session_state.filter_budget_min = budget_range[0]
            st.session_state.filter_budget_max = budget_range[1]
            st.query_params['budget_min'] = str(budget_range[0])
            st.query_params['budget_max'] = str(budget_range[1])
    
    with col2:
        all_countries = set()
        for colleges in colleges_data.values():
            for college in colleges:
                all_countries.add(college.get('country', 'Unknown'))
        country_filter = st.multiselect("Filter by Country", sorted(all_countries), default=st.session_state.filter_countries, key="country_select")
        if country_filter != st.session_state.filter_countries:
            st.session_state.filter_countries = country_filter
            if country_filter:
                st.query_params['countries'] = ','.join(country_filter)
            elif 'countries' in st.query_params:
                del st.query_params['countries']
    
    with col3:
        min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=st.session_state.filter_min_rating, step=0.1, key="rating_slider")
        if min_rating != st.session_state.filter_min_rating:
            st.session_state.filter_min_rating = min_rating
            st.query_params['min_rating'] = str(min_rating)
    
    col4, col5 = st.columns(2)
    
    with col4:
        all_durations = set()
        for colleges in colleges_data.values():
            for college in colleges:
                all_durations.add(college['duration'])
        duration_filter = st.multiselect("Filter by Duration", sorted(all_durations), default=st.session_state.filter_durations, key="duration_select")
        if duration_filter != st.session_state.filter_durations:
            st.session_state.filter_durations = duration_filter
            if duration_filter:
                st.query_params['durations'] = ','.join(duration_filter)
            elif 'durations' in st.query_params:
                del st.query_params['durations']
    
    with col5:
        search_query = st.text_input("🔍 Search Colleges", value=st.session_state.filter_search, key="search_input")
        if search_query != st.session_state.filter_search:
            st.session_state.filter_search = search_query
            st.query_params['search'] = search_query
    
    st.markdown("---")
    
    if st.session_state.show_college_detail:
        college = st.session_state.show_college_detail
        st.markdown("### 📋 College Profile")
        
        st.markdown(f"""
            <div class="college-detail-box">
                <h2>🏛️ {college['name']}</h2>
                <hr style="border: 1px solid #FF6B35; margin: 15px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown("#### 📍 Location & Contact")
            st.write(f"**Location:** {college['location']}")
            st.write(f"**Country:** {college['country']}")
            st.write(f"**Website:** [{college['contact']}]({college['contact']})")
            st.write(f"**Email:** {college['email']}")
            
            st.markdown("#### 💰 Financial Information")
            st.metric("Annual Tuition", f"${college['tuition']:,}")
            st.write(f"**Program Duration:** {college['duration']}")
        
        with detail_col2:
            st.markdown("#### 🎓 Accreditation & Quality")
            st.write(f"**Accreditation:** {college['accreditation']}")
            st.metric("Rating", f"{college['rating']}/5.0")
            st.write("⭐" * int(college['rating']))
            
            st.markdown("#### 🏢 Facilities")
            st.write(college['facilities'])
        
        st.markdown("---")
        st.markdown("### 📧 Contact This College")
        
        with st.expander("✉️ Send Inquiry Email"):
            st.write(f"Ready to reach out to {college['name']}?")
            st.write(f"Click below to send an email inquiry:")
            st.markdown(f"[📨 Email {college['name']}](mailto:{college['email']}?subject=Inquiry%20about%20Programs&body=Hello%2C%0A%0AI%20am%20interested%20in%20learning%20more%20about%20your%20programs.%0A%0AThank%20you!)", unsafe_allow_html=True)
            st.write(f"Or visit their website: [{college['contact']}]({college['contact']})")
        
        col_back, col_fav = st.columns([3, 1])
        with col_back:
            if st.button("⬅️ Back to College List", use_container_width=True):
                st.session_state.show_college_detail = None
                st.rerun()
        
        with col_fav:
            if is_favorite('college', college['name']):
                if st.button("💔 Unfavorite", use_container_width=True):
                    remove_favorite('college', college['name'])
                    st.rerun()
            else:
                if st.button("❤️ Favorite", use_container_width=True):
                    add_favorite('college', college['name'])
                    st.rerun()
    
    elif st.session_state.selected_course:
        colleges = colleges_data.get(st.session_state.selected_course, [])
        
        filtered_colleges = [
            college for college in colleges
            if budget_range[0] <= college["tuition"] <= budget_range[1]
            and (not country_filter or college.get('country', 'Unknown') in country_filter)
            and college['rating'] >= min_rating
            and (not duration_filter or college['duration'] in duration_filter)
            and (search_query.lower() in college["name"].lower() or 
                 search_query.lower() in college["location"].lower() or
                 search_query == "")
        ]
        
        st.subheader(f"Found {len(filtered_colleges)} college(s)")
        
        if filtered_colleges:
            for college in filtered_colleges:
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"### 🏛️ {college['name']}")
                    st.write(f"📍 {college['location']}")
                
                with col2:
                    st.metric("Annual Tuition", f"${college['tuition']:,}")
                    st.write(f"⏱️ Duration: {college['duration']}")
                
                with col3:
                    st.metric("Rating", f"{college['rating']}/5.0")
                    st.write("⭐" * int(college['rating']))
                
                with col4:
                    if st.button("ℹ️ Details", key=f"detail_{college['name']}"):
                        st.session_state.show_college_detail = college
                        st.rerun()
                    
                    if is_favorite('college', college['name']):
                        if st.button("💔", key=f"unfav_col_{college['name']}"):
                            remove_favorite('college', college['name'])
                            st.rerun()
                    else:
                        if st.button("❤️", key=f"fav_col_{college['name']}"):
                            add_favorite('college', college['name'])
                            st.rerun()
                
                st.markdown("---")
        else:
            st.warning("😔 No colleges found matching your criteria. Try adjusting your filters.")
    else:
        st.info("👈 Please select a course from the 'Browse Courses' page to view colleges!")

elif page == "📊 Compare Courses":
    st.header("📊 Course Comparison")
    
    if len(st.session_state.comparing_courses) < 2:
        st.info("Please add at least 2 courses to compare from the 'Browse Courses' page")
        st.write(f"Currently selected: {len(st.session_state.comparing_courses)} course(s)")
        if st.session_state.comparing_courses:
            for course in st.session_state.comparing_courses:
                st.write(f"- {courses_data[course]['icon']} {course}")
    else:
        st.success(f"Comparing {len(st.session_state.comparing_courses)} courses")
        
        st.markdown("### Overview Comparison")
        cols = st.columns(len(st.session_state.comparing_courses))
        
        for idx, course_name in enumerate(st.session_state.comparing_courses):
            with cols[idx]:
                course_info = courses_data[course_name]
                st.markdown(f"""
                    <div class="comparison-card">
                        <h3 style="text-align: center;">{course_info['icon']}</h3>
                        <h4 style="text-align: center;">{course_name}</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.write(course_info['description'])
                
                colleges = colleges_data.get(course_name, [])
                avg_tuition = sum(c['tuition'] for c in colleges) / len(colleges) if colleges else 0
                avg_rating = sum(c['rating'] for c in colleges) / len(colleges) if colleges else 0
                min_tuition = min(c['tuition'] for c in colleges) if colleges else 0
                max_tuition = max(c['tuition'] for c in colleges) if colleges else 0
                
                st.metric("# of Colleges", len(colleges))
                st.metric("Avg. Tuition", f"${avg_tuition:,.0f}")
                st.metric("Tuition Range", f"${min_tuition:,} - ${max_tuition:,}")
                st.metric("Avg. Rating", f"{avg_rating:.1f}/5.0")
                
                if st.button(f"Remove", key=f"remove_cmp_{course_name}", use_container_width=True):
                    st.session_state.comparing_courses.remove(course_name)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Detailed Comparison Table")
        
        comparison_data = []
        for course_name in st.session_state.comparing_courses:
            colleges = colleges_data.get(course_name, [])
            avg_tuition = sum(c['tuition'] for c in colleges) / len(colleges) if colleges else 0
            min_tuition = min(c['tuition'] for c in colleges) if colleges else 0
            max_tuition = max(c['tuition'] for c in colleges) if colleges else 0
            avg_rating = sum(c['rating'] for c in colleges) / len(colleges) if colleges else 0
            max_rating = max(c['rating'] for c in colleges) if colleges else 0
            
            duration_types = set(c['duration'] for c in colleges)
            countries = set(c['country'] for c in colleges)
            
            comparison_data.append({
                'Course': course_name,
                'Total Colleges': len(colleges),
                'Avg Tuition': f"${avg_tuition:,.0f}",
                'Min Tuition': f"${min_tuition:,.0f}",
                'Max Tuition': f"${max_tuition:,.0f}",
                'Avg Rating': f"{avg_rating:.2f}",
                'Max Rating': f"{max_rating:.1f}",
                'Duration Options': len(duration_types),
                'Countries Available': len(countries)
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### Top Colleges by Course")
        
        comp_cols = st.columns(len(st.session_state.comparing_courses))
        
        for idx, course_name in enumerate(st.session_state.comparing_courses):
            with comp_cols[idx]:
                st.markdown(f"#### {courses_data[course_name]['icon']} {course_name}")
                colleges = colleges_data.get(course_name, [])
                top_colleges = sorted(colleges, key=lambda x: x['rating'], reverse=True)[:3]
                
                for i, college in enumerate(top_colleges, 1):
                    st.write(f"{i}. **{college['name']}** ({college['rating']}/5.0)")
                    st.write(f"   ${college['tuition']:,} - {college['duration']}")

elif page == "❤️ My Favorites":
    st.header("❤️ My Favorites")
    
    all_favorites = get_favorites()
    
    if not all_favorites:
        st.info("You haven't added any favorites yet. Go to 'Browse Courses' or 'View Colleges' to add some!")
    else:
        favorite_courses = [fav[1] for fav in all_favorites if fav[0] == 'course']
        favorite_colleges = [fav[1] for fav in all_favorites if fav[0] == 'college']
        
        if favorite_courses:
            st.subheader(f"📚 Favorite Courses ({len(favorite_courses)})")
            cols = st.columns(2)
            for idx, course_name in enumerate(favorite_courses):
                with cols[idx % 2]:
                    course_info = courses_data.get(course_name)
                    if course_info:
                        st.markdown(f"""
                            <div class="course-card">
                                <h3>{course_info['icon']} {course_name}</h3>
                                <p>{course_info['description']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(f"View Colleges", key=f"fav_view_{course_name}", use_container_width=True):
                                st.session_state.selected_course = course_name
                                st.query_params['course'] = course_name
                                st.info("Navigate to 'View Colleges' page!")
                        with col_b:
                            if st.button("💔 Remove", key=f"fav_remove_{course_name}", use_container_width=True):
                                remove_favorite('course', course_name)
                                st.rerun()
            st.markdown("---")
        
        if favorite_colleges:
            st.subheader(f"🏛️ Favorite Colleges ({len(favorite_colleges)})")
            for college_name in favorite_colleges:
                found_college = None
                for colleges in colleges_data.values():
                    for college in colleges:
                        if college['name'] == college_name:
                            found_college = college
                            break
                    if found_college:
                        break
                
                if found_college:
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### 🏛️ {found_college['name']}")
                        st.write(f"📍 {found_college['location']}")
                    
                    with col2:
                        st.metric("Annual Tuition", f"${found_college['tuition']:,}")
                        st.write(f"⏱️ Duration: {found_college['duration']}")
                    
                    with col3:
                        st.metric("Rating", f"{found_college['rating']}/5.0")
                    
                    with col4:
                        if st.button("ℹ️ View", key=f"fav_detail_{college_name}"):
                            st.session_state.show_college_detail = found_college
                            st.rerun()
                        if st.button("💔", key=f"fav_col_remove_{college_name}"):
                            remove_favorite('college', college_name)
                            st.rerun()
                    
                    st.markdown("---")

st.markdown("---")
st.markdown("*Explore your culinary passion and find the perfect institution for your journey!* 🍴")
