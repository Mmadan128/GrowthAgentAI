
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Any

from main import (
    CareerPathfinderAgent, 
    UserProfile, 
    Skill, 
    Interest, 
    CareerGoal,
    SkillLevel, 
    CareerStage, 
    LearningStyle, 
    Industry
)


st.set_page_config(
    page_title="Career Pathfinder Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

if 'agent' not in st.session_state:
    st.session_state.agent = CareerPathfinderAgent()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'assessment_results' not in st.session_state:
    st.session_state.assessment_results = None
if 'learning_path' not in st.session_state:
    st.session_state.learning_path = None
if 'career_roadmap' not in st.session_state:
    st.session_state.career_roadmap = None

def main():
    """Main Streamlit app"""

    st.markdown('<h1 class="main-header">🚀 Career Pathfinder Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your AI-powered lifelong learning and career advisor</p>', unsafe_allow_html=True)

    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Dashboard", "👤 Profile Creation", "🔍 Skills Assessment", "📚 Learning Path", "🗺️ Career Roadmap", "💼 Job Market", "📊 Analytics", "⚙️ Settings"]
    )

    check_api_keys()

    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "👤 Profile Creation":
        show_profile_creation()
    elif page == "🔍 Skills Assessment":
        show_skills_assessment()
    elif page == "📚 Learning Path":
        show_learning_path()
    elif page == "🗺️ Career Roadmap":
        show_career_roadmap()
    elif page == "💼 Job Market":
        show_job_market()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def check_api_keys():
    """Check and display API key status"""
    required_vars = ['PORTIA_API_KEY']
    optional_llm_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY']
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    available_llm = [var for var in optional_llm_vars if os.getenv(var)]
    
    if missing_required:
        st.sidebar.error(f"⚠️ Missing: {', '.join(missing_required)}")
    else:
        st.sidebar.success("✅ PORTIA_API_KEY found")
    
    if available_llm:
        st.sidebar.info(f"🤖 LLM: {', '.join(available_llm)}")
    else:
        st.sidebar.warning("⚠️ No LLM API keys found")

def show_dashboard():
    """Show the main dashboard"""
    st.markdown('<h2 class="sub-header">📊 Your Career Dashboard</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.info("👋 Welcome! Please create a profile to get started.")
        st.markdown("""
        ### 🚀 What this agent can do for you:
        - **Skills Assessment**: Evaluate your current skills and identify gaps
        - **Learning Recommendations**: Get personalized learning resources
        - **Career Roadmapping**: Plan your career progression with timelines
        - **Job Market Analysis**: Understand market trends and opportunities
        - **Weekly Guidance**: Get personalized weekly recommendations
        
        ### 🎯 Getting Started:
        1. Go to **Profile Creation** to set up your profile
        2. Use **Skills Assessment** to evaluate your current state
        3. Generate a **Learning Path** for skill development
        4. Create a **Career Roadmap** for your goals
        """)
        return
    
    user = st.session_state.current_user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Current Role", user.current_role)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Experience", f"{user.years_experience} years")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Skills", len(user.skills))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Assess Skills", use_container_width=True):
            st.session_state.assessment_results = st.session_state.agent.assess_skills_and_goals(user.user_id)
            st.success("Skills assessment completed!")
    
    with col2:
        if st.button("📚 Generate Learning Path", use_container_width=True):
            target_skills = ["Machine Learning", "Data Science", "Leadership"]
            st.session_state.learning_path = st.session_state.agent.generate_learning_path(user.user_id, target_skills)
            st.success("Learning path generated!")
    
    with col3:
        if st.button("🗺️ Create Career Roadmap", use_container_width=True):
            st.session_state.career_roadmap = st.session_state.agent.create_career_roadmap(user.user_id, "Data Scientist")
            st.success("Career roadmap created!")

    if st.session_state.assessment_results:
        st.markdown("### 📋 Recent Assessment Results")
        st.json(st.session_state.assessment_results)

def show_profile_creation():
    """Show profile creation form"""
    st.markdown('<h2 class="sub-header">👤 Create Your Career Profile</h2>', unsafe_allow_html=True)
    
    with st.form("profile_creation"):
        st.markdown("### 📝 Basic Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g., Alex Johnson")
            email = st.text_input("Email", placeholder="alex.johnson@email.com")
            current_role = st.text_input("Current Job Title", placeholder="e.g., Data Analyst")
            current_company = st.text_input("Current Company", placeholder="e.g., TechCorp")
        
        with col2:
            years_experience = st.number_input("Years of Experience", min_value=0.0, max_value=50.0, value=3.0, step=0.5)
            education_level = st.selectbox("Education Level", [
                "High School", "Associate's", "Bachelor's", "Master's", "PhD", "Other"
            ])
            location_preference = st.text_input("Preferred Location", placeholder="e.g., San Francisco, CA")
        
        st.markdown("### 🎯 Career Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            career_stage = st.selectbox("Career Stage", [stage.value for stage in CareerStage])
            learning_style = st.selectbox("Learning Style", [style.value for style in LearningStyle])
        
        with col2:
            industry_preference = st.selectbox("Industry Preference", [industry.value for industry in Industry])
            salary_min = st.number_input("Salary Expectation (Min)", min_value=30000, value=60000, step=5000)
            salary_max = st.number_input("Salary Expectation (Max)", min_value=30000, value=120000, step=5000)
        
        st.markdown("### 🛠️ Current Skills")
        skills_input = st.text_area(
            "Skills (one per line or comma-separated)",
            placeholder="Python\nSQL\nData Visualization\nProject Management",
            help="Enter your skills, one per line or separated by commas"
        )
        
        st.markdown("### 🎯 Career Goals")
        career_goal = st.text_input("Main Career Goal", placeholder="e.g., Become a Data Scientist")
        goal_description = st.text_area("Goal Description", placeholder="Describe your career objective...")
        
        submitted = st.form_submit_button("🚀 Create Profile")
        
        if submitted:
            if name and current_role:
   
                if skills_input:
                    skills_list = []
                    for line in skills_input.replace(',', '\n').split('\n'):
                        skill_name = line.strip()
                        if skill_name:
                            skills_list.append(Skill(
                                name=skill_name,
                                level=SkillLevel.INTERMEDIATE,
                                relevance_score=8.0,
                                years_experience=1.0,
                                target_level=SkillLevel.ADVANCED
                            ))
                
                
                user_data = {
                    "user_id": f"user_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "name": name,
                    "email": email,
                    "current_role": current_role,
                    "current_company": current_company,
                    "career_stage": CareerStage(career_stage),
                    "years_experience": years_experience,
                    "education_level": education_level,
                    "learning_style": LearningStyle(learning_style),
                    "industry_preference": Industry(industry_preference),
                    "location_preference": location_preference,
                    "salary_expectations": (salary_min, salary_max),
                    "skills": skills_list,
                    "interests": [],
                    "career_goals": [CareerGoal(
                        title=career_goal,
                        description=goal_description,
                        priority=1
                    )] if career_goal else []
                }
                
                try:
                    profile = st.session_state.agent.create_user_profile(user_data)
                    st.session_state.current_user = profile
                    st.success(f"🎉 Profile created successfully for {profile.name}!")
                    st.balloons()
                    
                    # Show profile summary
                    st.markdown("### 📋 Profile Summary")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**User ID:** {profile.user_id}")
                        st.write(f"**Name:** {profile.name}")
                        st.write(f"**Current Role:** {profile.current_role}")
                        st.write(f"**Experience:** {profile.years_experience} years")
                    
                    with col2:
                        st.write(f"**Career Stage:** {profile.career_stage.value}")
                        st.write(f"**Industry:** {profile.industry_preference.value}")
                        st.write(f"**Skills:** {len(profile.skills)} skills")
                        st.write(f"**Goals:** {len(profile.career_goals)} goals")
                    
                except Exception as e:
                    st.error(f"❌ Error creating profile: {e}")
            else:
                st.error("Please fill in at least your name and current role.")

def show_skills_assessment():
    """Show skills assessment interface"""
    st.markdown('<h2 class="sub-header">🔍 Skills Assessment & Analysis</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.warning("⚠️ Please create a profile first to assess skills.")
        return
    
    user = st.session_state.current_user
    

    st.markdown("### 👤 Current Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {user.name}")
        st.write(f"**Current Role:** {user.current_role}")
        st.write(f"**Career Stage:** {user.career_stage.value}")
        st.write(f"**Experience:** {user.years_experience} years")
    
    with col2:
        st.write(f"**Industry:** {user.industry_preference.value}")
        st.write(f"**Learning Style:** {user.learning_style.value}")
        st.write(f"**Skills Count:** {len(user.skills)}")
        st.write(f"**Goals Count:** {len(user.career_goals)}")
    

    if user.skills:
        st.markdown("### 🛠️ Current Skills Analysis")
        

        skills_df = pd.DataFrame([
            {
                'Skill': skill.name,
                'Level': skill.level.value,
                'Experience': skill.years_experience,
                'Relevance': skill.relevance_score
            }
            for skill in user.skills
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_level = px.bar(
                skills_df, 
                x='Skill', 
                y='Experience',
                title="Skills by Experience (Years)",
                color='Level',
                color_discrete_map={
                    'beginner': '#ff7f0e',
                    'intermediate': '#2ca02c',
                    'advanced': '#1f77b4',
                    'expert': '#d62728'
                }
            )
            st.plotly_chart(fig_level, use_container_width=True)
        
        with col2:
            fig_relevance = px.scatter(
                skills_df,
                x='Experience',
                y='Relevance',
                size='Relevance',
                color='Skill',
                title="Skills Relevance vs Experience",
                hover_data=['Skill', 'Level']
            )
            st.plotly_chart(fig_relevance, use_container_width=True)
    
    if st.button("🔍 Run Comprehensive Skills Assessment", type="primary", use_container_width=True):
        with st.spinner("Analyzing your skills and career goals..."):
            try:
                assessment = st.session_state.agent.assess_skills_and_goals(user.user_id)
                st.session_state.assessment_results = assessment
                st.success("✅ Skills assessment completed!")

                st.markdown("### 📊 Assessment Results")
                
                if isinstance(assessment, dict):

                    if 'skill_gaps' in assessment:
                        st.markdown("#### 🎯 Identified Skill Gaps")
                        for gap in assessment['skill_gaps']:
                            st.write(f"• {gap}")
                    
                    if 'career_recommendations' in assessment:
                        st.markdown("#### 💡 Career Recommendations")
                        for rec in assessment['career_recommendations']:
                            st.write(f"• {rec}")
                    

                    if 'learning_priorities' in assessment:
                        st.markdown("#### 📚 Learning Priorities")
                        for priority in assessment['learning_priorities']:
                            st.write(f"• {priority}")
                    
                    # Timeline
                    if 'timeline_suggestions' in assessment:
                        st.markdown("#### ⏰ Timeline Suggestions")
                        st.info(assessment['timeline_suggestions'])
                    
                    # Risk factors
                    if 'risk_factors' in assessment:
                        st.markdown("#### ⚠️ Risk Factors")
                        for risk in assessment['risk_factors']:
                            st.write(f"• {risk}")
                    
                    # Mitigation strategies
                    if 'mitigation_strategies' in assessment:
                        st.markdown("#### 🛡️ Mitigation Strategies")
                        for strategy in assessment['mitigation_strategies']:
                            st.write(f"• {strategy}")
                
            except Exception as e:
                st.error(f"❌ Assessment failed: {e}")
                st.info("Using fallback assessment data...")

def show_learning_path():
    """Show learning path generation interface"""
    st.markdown('<h2 class="sub-header">📚 Personalized Learning Path</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.warning("⚠️ Please create a profile first to generate learning paths.")
        return
    
    user = st.session_state.current_user
    
    # Target skills input
    st.markdown("### 🎯 Select Target Skills")
    
    # Predefined skill categories
    skill_categories = {
        "Data Science & ML": ["Python", "Machine Learning", "Deep Learning", "Statistics", "Data Analysis"],
        "Programming": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
        "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD"],
        "Business Skills": ["Leadership", "Project Management", "Communication", "Strategic Thinking"],
        "Domain Knowledge": ["Finance", "Healthcare", "E-commerce", "Cybersecurity", "AI Ethics"]
    }
    
    selected_category = st.selectbox("Choose skill category:", list(skill_categories.keys()))
    available_skills = skill_categories[selected_category]
    
    target_skills = st.multiselect(
        "Select skills to develop:",
        options=available_skills,
        default=available_skills[:3] if len(available_skills) >= 3 else available_skills
    )
    
    # Custom skills input
    custom_skills = st.text_input("Add custom skills (comma-separated):", placeholder="e.g., Blockchain, Quantum Computing")
    if custom_skills:
        custom_skills_list = [skill.strip() for skill in custom_skills.split(',') if skill.strip()]
        target_skills.extend(custom_skills_list)
    
    # Learning preferences
    st.markdown("### 🎓 Learning Preferences")
    col1, col2 = st.columns(2)
    
    with col1:
        max_budget = st.slider("Maximum Budget ($)", 0, 1000, 200, step=50)
        max_duration = st.slider("Maximum Duration (hours)", 10, 200, 60, step=10)
    
    with col2:
        difficulty_level = st.selectbox("Preferred Difficulty", ["beginner", "intermediate", "advanced", "expert"])
        learning_platform = st.multiselect(
            "Preferred Platforms",
            ["Coursera", "edX", "Udemy", "DataCamp", "Pluralsight", "YouTube", "Books"],
            default=["Coursera", "edX"]
        )
    
    # Generate learning path
    if st.button("🚀 Generate Learning Path", type="primary", use_container_width=True):
        if target_skills:
            with st.spinner("Generating personalized learning path..."):
                try:
                    learning_path = st.session_state.agent.generate_learning_path(user.user_id, target_skills)
                    st.session_state.learning_path = learning_path
                    st.success(f"✅ Learning path generated with {len(learning_path)} resources!")
                    
                    # Display learning path
                    st.markdown("### 📚 Your Learning Path")
                    
                    for i, resource in enumerate(learning_path, 1):
                        with st.expander(f"{i}. {resource.title}", expanded=True):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Platform:** {resource.platform}")
                                st.write(f"**Skills Covered:** {', '.join(resource.skills_covered)}")
                                st.write(f"**Difficulty:** {resource.difficulty.title()}")
                                st.write(f"**Duration:** {resource.duration_hours} hours")
                            
                            with col2:
                                st.write(f"**Rating:** ⭐ {resource.rating}/5.0")
                                st.write(f"**Cost:** ${resource.cost}")
                                st.write(f"**Status:** {resource.completion_status.replace('_', ' ').title()}")
                            
                            if resource.url:
                                st.link_button("🔗 Visit Course", resource.url)
                    
                    # Learning path summary
                    st.markdown("### 📊 Learning Path Summary")
                    total_cost = sum(r.cost for r in learning_path)
                    total_duration = sum(r.duration_hours for r in learning_path)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Resources", len(learning_path))
                    with col2:
                        st.metric("Total Cost", f"${total_cost}")
                    with col3:
                        st.metric("Total Duration", f"{total_duration} hours")
                    
                except Exception as e:
                    st.error(f"❌ Learning path generation failed: {e}")
                    st.info("Using fallback learning recommendations...")
        else:
            st.warning("⚠️ Please select at least one target skill.")

def show_career_roadmap():
    """Show career roadmap creation interface"""
    st.markdown('<h2 class="sub-header">🗺️ Career Roadmap Creation</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.warning("⚠️ Please create a profile first to create career roadmaps.")
        return
    
    user = st.session_state.current_user
    
    with st.form("roadmap_creation"):
        st.markdown("### 🎯 Define Your Career Goal")
        
        col1, col2 = st.columns(2)
        with col1:
            target_role = st.text_input("Target Role", placeholder="e.g., Data Scientist", value="Data Scientist")
            timeline_months = st.slider("Target Timeline (months)", 6, 60, 18, step=3)
        
        with col2:
            priority_level = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
            industry_focus = st.selectbox("Industry Focus", [industry.value for industry in Industry])
        
        additional_context = st.text_area(
            "Additional Context (optional)",
            placeholder="Describe any specific requirements, constraints, or preferences for your career transition...",
            help="This helps the AI create a more personalized roadmap"
        )
        
        submitted = st.form_submit_button("🗺️ Create Career Roadmap", type="primary")
        
        if submitted:
            if target_role:
                with st.spinner("Creating your personalized career roadmap..."):
                    try:
                        roadmap = st.session_state.agent.create_career_roadmap(user.user_id, target_role)
                        st.session_state.career_roadmap = roadmap
                        st.success("✅ Career roadmap created successfully!")
                        
                        display_roadmap(roadmap)
                        
                    except Exception as e:
                        st.error(f"❌ Roadmap creation failed: {e}")
                        st.info("Using fallback career roadmap...")
            else:
                st.warning("⚠️ Please specify a target role.")

def display_roadmap(roadmap):
    """Display the career roadmap in an attractive format"""
    st.markdown("### 🗺️ Your Career Roadmap")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("From", roadmap.current_position)
    with col2:
        st.metric("To", roadmap.target_position)
    with col3:
        st.metric("Timeline", f"{roadmap.timeline_months} months")

    if roadmap.milestones:
        st.markdown("#### 📅 Key Milestones")
        
        timeline_data = []
        for milestone in roadmap.milestones:
            if isinstance(milestone, dict) and 'month' in milestone and 'milestone' in milestone:
                timeline_data.append({
                    'Month': milestone['month'],
                    'Milestone': milestone['milestone']
                })
        
        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)

            fig = go.Figure()
            
            for idx, row in timeline_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['Month'], row['Month'] + 1],
                    y=[row['Milestone'], row['Milestone']],
                    mode='lines+markers',
                    name=f"Month {row['Month']}",
                    line=dict(width=8, color=f'rgb({100 + idx*50}, {150 + idx*30}, {200 + idx*40})'),
                    marker=dict(size=12)
                ))
            
            fig.update_layout(
                title="Career Progression Timeline",
                xaxis_title="Month",
                yaxis_title="Milestones",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    if roadmap.skill_gaps:
        st.markdown("#### 🎯 Skills to Develop")
        for gap in roadmap.skill_gaps:
            st.write(f"• {gap}")
    
    if roadmap.market_analysis:
        st.markdown("#### 💼 Market Analysis")
        market_cols = st.columns(len(roadmap.market_analysis))
        for i, (key, value) in enumerate(roadmap.market_analysis.items()):
            with market_cols[i]:
                st.metric(key.replace('_', ' ').title(), value)

    if roadmap.risk_factors:
        st.markdown("#### ⚠️ Risk Factors")
        for risk in roadmap.risk_factors:
            st.write(f"• {risk}")

def show_job_market():
    """Show job market analysis interface"""
    st.markdown('<h2 class="sub-header">💼 Job Market Analysis</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.warning("⚠️ Please create a profile first to analyze job markets.")
        return
    
    user = st.session_state.current_user
    
    with st.form("job_market_analysis"):
        st.markdown("### 🔍 Analyze Job Market")
        
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist", value="Data Scientist")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA", value=user.location_preference)
        
        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead", "Executive"])
            remote_preference = st.checkbox("Remote Work Preferred")
        
        if user.skills:
            st.markdown("### 🛠️ Skills Filter")
            available_skills = [skill.name for skill in user.skills]
            selected_skills = st.multiselect(
                "Select relevant skills:",
                options=available_skills,
                default=available_skills[:5] if len(available_skills) >= 5 else available_skills
            )
        else:
            selected_skills = ["Python", "Data Analysis", "Machine Learning"]
        
        submitted = st.form_submit_button("🔍 Analyze Job Market", type="primary")
        
        if submitted:
            if job_title and location:
                with st.spinner("Analyzing job market trends..."):
                    try:
                        market_analysis = st.session_state.agent.analyze_job_market(job_title, location, selected_skills)
                        st.success("✅ Job market analysis completed!")
                        
                        # Display results
                        display_job_market_analysis(market_analysis)
                        
                    except Exception as e:
                        st.error(f"❌ Job market analysis failed: {e}")
                        st.info("Using fallback job market analysis...")
            else:
                st.warning("⚠️ Please specify job title and location.")

def display_job_market_analysis(analysis):
    """Display job market analysis results"""
    st.markdown("### 📊 Job Market Analysis Results")
    
    if isinstance(analysis, dict):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'market_demand' in analysis:
                st.metric("Market Demand", analysis['market_demand'])
        
        with col2:
            if 'average_salary' in analysis:
                st.metric("Average Salary", analysis['average_salary'])
        
        with col3:
            if 'job_growth' in analysis:
                st.metric("Job Growth", analysis['job_growth'])
        
        with col4:
            if 'competition_level' in analysis:
                st.metric("Competition", analysis['competition_level'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'required_skills' in analysis:
                st.markdown("#### 🛠️ Required Skills")
                for skill in analysis['required_skills']:
                    st.write(f"• {skill}")
            
            if 'top_companies' in analysis:
                st.markdown("#### 🏢 Top Companies")
                for company in analysis['top_companies']:
                    st.write(f"• {company}")
        
        with col2:
            if 'emerging_trends' in analysis:
                st.markdown("#### 🚀 Emerging Trends")
                for trend in analysis['emerging_trends']:
                    st.write(f"• {trend}")
            
            if 'remote_opportunities' in analysis:
                st.markdown("#### 🏠 Remote Opportunities")
                st.info(analysis['remote_opportunities'])

def show_analytics():
    """Show analytics and insights"""
    st.markdown('<h2 class="sub-header">📊 Career Analytics & Insights</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_user is None:
        st.warning("⚠️ Please create a profile first to view analytics.")
        return
    
    user = st.session_state.current_user
    
    if user.skills:
        st.markdown("### 🎯 Skills Radar Chart")
        
        skills_data = []
        for skill in user.skills:
            skills_data.append({
                'Skill': skill.name,
                'Level': skill.level.value,
                'Experience': skill.years_experience,
                'Relevance': skill.relevance_score
            })
        
        skills_df = pd.DataFrame(skills_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=skills_df['Relevance'],
            theta=skills_df['Skill'],
            fill='toself',
            name='Skill Relevance',
            line_color='rgb(32, 201, 151)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            title="Skills Relevance Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.career_roadmap:
        st.markdown("### 📈 Career Progression")
        roadmap = st.session_state.career_roadmap
        

        if roadmap.milestones:
            milestone_data = []
            for milestone in roadmap.milestones:
                if isinstance(milestone, dict) and 'month' in milestone:
                    milestone_data.append({
                        'Month': milestone['month'],
                        'Progress': (milestone['month'] / roadmap.timeline_months) * 100
                    })
            
            if milestone_data:
                progress_df = pd.DataFrame(milestone_data)
                
                fig = px.line(
                    progress_df,
                    x='Month',
                    y='Progress',
                    title="Career Progression Timeline",
                    markers=True
                )
                
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Progress (%)",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)

    if st.session_state.learning_path:
        st.markdown("### 📚 Learning Path Analytics")
        learning_path = st.session_state.learning_path
        

        platform_data = {}
        for resource in learning_path:
            platform = resource.platform
            if platform not in platform_data:
                platform_data[platform] = {'count': 0, 'total_cost': 0, 'total_duration': 0}
            platform_data[platform]['count'] += 1
            platform_data[platform]['total_cost'] += resource.cost
            platform_data[platform]['total_duration'] += resource.duration_hours
        
        platform_df = pd.DataFrame([
            {
                'Platform': platform,
                'Resources': data['count'],
                'Total Cost': data['total_cost'],
                'Total Duration': data['total_duration']
            }
            for platform, data in platform_data.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_platform = px.pie(
                platform_df,
                values='Resources',
                names='Platform',
                title="Resources by Platform"
            )
            st.plotly_chart(fig_platform, use_container_width=True)
        
        with col2:
            fig_cost = px.bar(
                platform_df,
                x='Platform',
                y='Total Cost',
                title="Total Cost by Platform"
            )
            st.plotly_chart(fig_cost, use_container_width=True)

def show_settings():
    """Show settings and configuration"""
    st.markdown('<h2 class="sub-header">⚙️ Settings & Configuration</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Configuration")
    
    api_keys = {
        'PORTIA_API_KEY': os.getenv('PORTIA_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
    }
    
    for key_name, key_value in api_keys.items():
        if key_value:
            st.success(f"✅ {key_name}: {'*' * (len(key_value) - 8) + key_value[-8:]}")
        else:
            st.error(f"❌ {key_name}: Not set")
    
    st.markdown("### 📁 Environment Variables")
    st.info("""
    To configure API keys, create a `.env` file in your project directory with:
    
    ```
    PORTIA_API_KEY=your_portia_api_key_here
    GOOGLE_API_KEY=your_google_api_key_here
    # Optional: Other LLM providers
    OPENAI_API_KEY=your_openai_api_key_here
    ANTHROPIC_API_KEY=your_anthropic_api_key_here
    ```
    """)
    
    st.markdown("### 🗑️ Reset Data")
    if st.button("Clear All Data", type="secondary"):
        st.session_state.current_user = None
        st.session_state.assessment_results = None
        st.session_state.learning_path = None
        st.session_state.career_roadmap = None
        st.success("✅ All data cleared!")

if __name__ == "__main__":
    main()
