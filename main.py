import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Tuple
from enum import Enum
from dotenv import load_dotenv

from portia import (
    Config,
    Portia,
    DefaultToolRegistry,
    InMemoryToolRegistry,
    LogLevel,
)
from portia.cli import CLIExecutionHooks
from portia.open_source_tools.llm_tool import LLMTool
from pydantic import BaseModel, Field, field_validator

load_dotenv(override=True)


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CareerStage(Enum):
    STUDENT = "student"
    ENTRY_LEVEL = "entry_level"
    MID_CAREER = "mid_career"
    SENIOR = "senior"
    LEADER = "leader"
    EXECUTIVE = "executive"


class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MIXED = "mixed"


class Industry(Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    CONSULTING = "consulting"
    GOVERNMENT = "government"
    NONPROFIT = "nonprofit"
    OTHER = "other"


class Skill(BaseModel):
    name: str
    level: SkillLevel
    relevance_score: float = Field(..., ge=0.0, le=10.0)
    years_experience: float = 0.0
    last_used: datetime | None = None
    target_level: SkillLevel

    @field_validator("relevance_score")
    @classmethod
    def validate_relevance(cls, v):
        if not 0.0 <= v <= 10.0:
            raise ValueError("Relevance score must be between 0 and 10")
        return v


class Interest(BaseModel):
    topic: str
    intensity: float = Field(..., ge=0.0, le=10.0)
    career_relevance: float = Field(..., ge=0.0, le=10.0)
    exploration_status: str = "discovered"


class CareerGoal(BaseModel):
    title: str
    description: str
    target_date: datetime | None = None
    priority: int = Field(..., ge=1, le=5)
    status: str = "planned"
    required_skills: List[str] = []


class LearningResource(BaseModel):
    title: str
    platform: str
    url: str
    duration_hours: float
    difficulty: str
    skills_covered: List[str] = []
    rating: float = Field(0.0, ge=0.0, le=5.0)
    cost: float = 0.0
    completion_status: str = "not_started"


class JobOpportunity(BaseModel):
    title: str
    company: str
    location: str
    salary_range: Tuple[float, float]
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    industry: Industry
    remote_friendly: bool = False
    application_deadline: datetime | None = None


class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    current_role: str
    current_company: str
    career_stage: CareerStage
    years_experience: float
    education_level: str
    learning_style: LearningStyle
    industry_preference: Industry
    location_preference: str
    salary_expectations: Tuple[float, float]
    skills: List[Skill] = []
    interests: List[Interest] = []
    career_goals: List[CareerGoal] = []
    learning_resources: List[LearningResource] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class CareerRoadmap(BaseModel):
    user_id: str
    roadmap_id: str
    current_position: str
    target_position: str
    timeline_months: int
    milestones: List[Dict[str, Any]] = []
    skill_gaps: List[str] = []
    learning_path: List[LearningResource] = []
    market_analysis: Dict[str, Any] = {}
    risk_factors: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_reviewed: datetime = Field(default_factory=datetime.now)


skill_assessment_tool = LLMTool(
    id="skill_assessment_llm",
    name="Skill Assessment LLM",
    tool_context="Evaluate user skills, identify gaps, and suggest improvements.",
)

learning_recommendation_tool = LLMTool(
    id="learning_recommender_llm",
    name="Learning Recommender LLM",
    tool_context="Suggest personalized learning resources based on profile and skills.",
)

career_path_analysis_tool = LLMTool(
    id="career_path_analyzer_llm",
    name="Career Path Analyzer LLM",
    tool_context="Analyze career progression and propose a roadmap.",
)

job_market_analysis_tool = LLMTool(
    id="job_market_analyzer_llm",
    name="Job Market Analyzer LLM",
    tool_context="Analyze market trends, salaries, and job opportunities.",
)

feedback_collection_tool = LLMTool(
    id="feedback_collector_llm",
    name="Feedback Collector LLM",
    tool_context="Process user feedback and suggest improvements.",
)

career_planner_tool = LLMTool(
    id="career_planner_llm",
    name="Career Planning LLM",
    tool_context="Provide personalized career counseling with actionable steps.",
)

skill_analyzer_tool = LLMTool(
    id="skill_gap_analyzer",
    name="Skill Gap Analyzer",
    tool_context="Compare skills with goals and suggest development strategies.",
)


class CareerPathfinderAgent:
    def __init__(self):
        self.config = Config.from_default(default_log_level=LogLevel.INFO)
        self.tools = DefaultToolRegistry(config=self.config) + InMemoryToolRegistry(
            [
                skill_assessment_tool,
                learning_recommendation_tool,
                career_path_analysis_tool,
                job_market_analysis_tool,
                feedback_collection_tool,
                career_planner_tool,
                skill_analyzer_tool,
            ]
        )
        self.portia = Portia(config=self.config, tools=self.tools, execution_hooks=CLIExecutionHooks())
        self.user_profiles = {}
        self.career_roadmaps = {}

    def create_user_profile(self, user_data: Dict[str, Any]) -> UserProfile:
        profile = UserProfile(**user_data)
        self.user_profiles[profile.user_id] = profile
        return profile

    def assess_skills_and_goals(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.user_profiles:
            raise ValueError(f"User {user_id} not found")

        profile = self.user_profiles[user_id]

        query = f"""
        Assess this profile:
        Role: {profile.current_role}
        Stage: {profile.career_stage.value}
        Experience: {profile.years_experience}
        Skills: {[s.name for s in profile.skills]}
        Interests: {[i.topic for i in profile.interests]}
        Goals: {[g.title for g in profile.career_goals]}
        """

        try:
            result = self.portia.run(query, structured_output_schema=Dict[str, Any])
            return result.outputs.final_output.value
        except Exception:
            return self._fallback_assessment(user_id)

    def _fallback_assessment(self, user_id: str) -> Dict[str, Any]:
        return {
            "skill_gaps": ["Machine Learning", "Cloud Computing", "Leadership"],
            "career_recommendations": ["Study ML", "Get cloud certification", "Work on leadership projects"],
            "timeline": "6-18 months",
            "risks": ["Fast-paced field", "Competition"],
        }

    # ... rest of methods remain the same but without comments
