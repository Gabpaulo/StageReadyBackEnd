"""All StageReady per-feature activity diagrams. Run: python diagrams.py <outdir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swimlane import render
U, A, S, B = "User", "Administrator", "StageReady App / Firebase", "AI Backend (FastAPI + RAG)"
L = lambda t: {"label": t}

D = {}

D["login_register"] = dict(title="Login / Register", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open StageReady"),
  "s1": ("act", S, 1, "Display login /\nregister form"),
  "u2": ("act", U, 2, "Choose Login, Register\nor Google sign-in"),
  "u3": ("act", U, 3, "Enter email and password\n(or pick Google account)"),
  "s3": ("act", S, 3, "Validate credentials\n(Firebase Auth)"),
  "d1": ("dec", S, 4, "Valid?"),
  "d2": ("dec", S, 5, "Onboarding\ncomplete?"),
  "u5": ("act", U, 5, "Complete onboarding\n(Complete Onboarding)"),
  "s6": ("act", S, 6, "Open dashboard"),
  "en": ("end", S, 7, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","u2","r"), ("u2","b","u3","t"), ("u3","r","s3","l"),
  ("s3","b","d1","t"), ("d1","l","u3","b", L("[no] show error")), ("d1","b","d2","t", L("[yes]")),
  ("d2","l","u5","r", L("[no]")), ("d2","b","s6","t", L("[yes]")), ("u5","b","s6","l"), ("s6","b","en","t"),
])

D["complete_challenges"] = dict(title="Complete Challenges", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open dashboard"),
  "s1": ("act", S, 1, "Load gamification record\n(userGamification)"),
  "s2": ("act", S, 2, "Show today's challenge\n(1 of 7) and XP reward"),
  "u3": ("act", U, 3, "Record a speech that\nfollows the challenge"),
  "s3": ("act", S, 3, "Analyze and save\nthe session"),
  "s4": ("act", S, 4, "Award XP for the\ncompleted speech"),
  "d1": ("dec", S, 5, "First speech\ntoday?"),
  "s6": ("act", S, 6, "Add first-speech-of-\nthe-day bonus XP"),
  "s7": ("act", S, 7, "Update streak and\ncheck for level-up"),
  "s8": ("act", S, 8, "Check badge unlocks\n(userBadges)"),
  "u9": ("act", U, 9, "View updated XP, level,\nstreak and badges"),
  "en": ("end", U, 10, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","s2","t"), ("s2","b","u3","r"), ("u3","r","s3","l"),
  ("s3","b","s4","t"), ("s4","b","d1","t"), ("d1","b","s6","t", L("[yes]")),
  ("d1","r","s7","r", {"label": "[no]", "via": [((S, 145), None), (None, (7,))]}),
  ("s6","b","s7","t"), ("s7","b","s8","t"), ("s8","b","u9","r"), ("u9","b","en","t"),
])

D["record_speech"] = dict(title="Record Speech", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Record Speech\nscreen"),
  "s1": ("act", S, 1, "Ask for speech type"),
  "u2": ("act", U, 2, "Select informative,\npersuasive or motivational"),
  "u3": ("act", U, 3, "Tap Record"),
  "s3": ("act", S, 3, "Request microphone\naccess"),
  "d1": ("dec", S, 4, "Access\ngranted?"),
  "s5": ("act", S, 5, "Capture audio, show timer\nand live audio levels"),
  "u6": ("act", U, 6, "Speak, then tap Stop"),
  "s6": ("act", S, 6, "Stop recording and\nprepare WAV audio"),
  "u7": ("act", U, 7, "Play back and review\nthe recording"),
  "d2": ("dec", U, 8, "Submit or\nre-record?"),
  "s9": ("act", S, 9, "Send audio for analysis\n(Receive AI Feedback)"),
  "en": ("end", S, 10, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","u2","r"), ("u2","b","u3","t"), ("u3","r","s3","l"),
  ("s3","b","d1","t"), ("d1","l","u3","b", L("[no] show error")), ("d1","b","s5","t", L("[yes]")),
  ("s5","b","u6","r"), ("u6","r","s6","l"), ("s6","b","u7","r"), ("u7","b","d2","t"),
  ("d2","l","u3","l", {"label": "[re-record]", "via": [((U, -150), None), (None, (3,))]}),
  ("d2","r","s9","t", L("[submit]")), ("s9","b","en","t"),
])

D["manage_profile"] = dict(title="Manage User Profile", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Profile page"),
  "s1": ("act", S, 1, "Retrieve profile\n(users/{uid})"),
  "s2": ("act", S, 2, "Display profile, interests\nand practice stats"),
  "u3": ("act", U, 3, "Tap Edit and change\ndetails or preferences"),
  "u4": ("act", U, 4, "Tap Save"),
  "s4": ("act", S, 4, "Validate input"),
  "d1": ("dec", S, 5, "Valid?"),
  "s6": ("act", S, 6, "Update users document\nin Firestore"),
  "s7": ("act", S, 7, "Refresh profile view"),
  "en": ("end", S, 8, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","s2","t"), ("s2","b","u3","r"), ("u3","b","u4","t"),
  ("u4","r","s4","l"), ("s4","b","d1","t"),
  ("d1","l","u3","l", {"label": "[no] show error", "via": [((U, -150), None), (None, (3,))]}),
  ("d1","b","s6","t", L("[yes]")), ("s6","b","s7","t"), ("s7","b","en","t"),
])

D["practice_recommendation"] = dict(title="Practice Recommendation", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Dashboard or\nPractice Mode"),
  "s1": ("act", S, 1, "Load last 30 sessions\n(speechHistory)"),
  "d1": ("dec", S, 2, "Any sessions?"),
  "u2": ("act", U, 2, "See prompt to record\na first session"),
  "e1": ("end", U, 3, ""),
  "s3": ("act", S, 3, "Compute average score\nper dimension"),
  "d2": ("dec", S, 4, "3 or more\nsessions?"),
  "s5a": ("act", S, 5, "Train regression\n(TensorFlow.js) to find\nhigh-impact dimensions", {"dx": -78, "w": 160}),
  "s5b": ("act", S, 5, "Use weakest\ndimensions\n(fallback)", {"dx": 88, "w": 140}),
  "s6": ("act", S, 6, "Set target difficulty\nand WPM goal"),
  "s7": ("act", S, 7, "Select recommended\nscripts"),
  "u8": ("act", U, 8, "View plan (AI badge\nwhen the model is used)"),
  "u9": ("act", U, 9, "Select a recommended\nscript"),
  "s9": ("act", S, 9, "Open Practice Mode with\nthe script pre-loaded"),
  "en": ("end", S, 10, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","d1","t"), ("d1","l","u2","r", L("[no]")), ("u2","b","e1","t"),
  ("d1","b","s3","t", L("[yes]")), ("s3","b","d2","t"),
  ("d2","l","s5a","t", L("[yes]")), ("d2","r","s5b","t", L("[no]")),
  ("s5a","b","s6","t", {"my": None}), ("s5b","b","s6","t"), ("s6","b","s7","t"), ("s7","b","u8","r"),
  ("u8","b","u9","t"), ("u9","r","s9","l"), ("s9","b","en","t"),
])

D["receive_feedback"] = dict(title="Receive AI Feedback", lanes=[U, S, B], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Submit recording"),
  "s1": ("act", S, 1, "Send audio and speech\ntype to the backend"),
  "b1": ("act", B, 1, "Transcribe audio\n(Groq Whisper)"),
  "b2": ("act", B, 2, "Extract acoustic features\n(pace, loudness, pitch,\npauses, fillers)"),
  "b3": ("act", B, 3, "Retrieve similar speeches\n(Corpus 1) and expert\nguidance (Corpus 2)"),
  "b4": ("act", B, 4, "Score 7 dimensions +\noverall and write feedback\n(LLM)"),
  "d1": ("dec", S, 5, "Analysis\nsucceeded?"),
  "s6": ("act", S, 6, "Save session to Firestore\n(speeches, speechHistory)"),
  "s7": ("act", S, 7, "Update XP, streak\nand badges"),
  "u8": ("act", U, 8, "View feedback report\n(scores, coaching tips)"),
  "en": ("end", U, 9, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","r","b1","l"), ("b1","b","b2","t"), ("b2","b","b3","t"),
  ("b3","b","b4","t"), ("b4","b","d1","r"), ("d1","l","u1","b", L("[no] show error, retry")),
  ("d1","b","s6","t", L("[yes]")), ("s6","b","s7","t"), ("s7","b","u8","r"), ("u8","b","en","t"),
])

D["manage_scripts"] = dict(title="Manage Practice Scripts", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open Practice Mode\nsection (admin app)"),
  "s1": ("act", S, 1, "Load all scripts\n(practiceScripts)"),
  "a2": ("act", A, 2, "Choose add, edit,\nactivate/deactivate\nor delete"),
  "s2": ("act", S, 2, "Show script form or\nconfirmation dialog"),
  "a3": ("act", A, 3, "Enter script details\nor confirm"),
  "s3": ("act", S, 3, "Validate script\n(title, text, targets)"),
  "d1": ("dec", S, 4, "Valid?"),
  "s5": ("act", S, 5, "Save to practiceScripts"),
  "s6": ("act", S, 6, "Refresh list (active\nscripts reach all users)"),
  "en": ("end", S, 7, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","a2","r"), ("a2","r","s2","l"), ("s2","b","a3","r"),
  ("a3","r","s3","l"), ("s3","b","d1","t"), ("d1","l","a3","b", L("[no] show error")),
  ("d1","b","s5","t", L("[yes]")), ("s5","b","s6","t"), ("s6","b","en","t"),
])

D["knowledge_base"] = dict(title="View Knowledge Base", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Knowledge Base"),
  "s1": ("act", S, 1, "Load curated resources\nand quiz section"),
  "u2": ("act", U, 2, "Filter resources\nby category"),
  "s2": ("act", S, 2, "Show filtered list"),
  "d1": ("dec", U, 3, "Open resource\nor take quiz?", {"w": 150}),
  "s3": ("act", S, 3, "Start personalized quiz\n(Take Quiz)", {"dx": -25, "w": 200}),
  "eq": ("end", S, 3, "", {"dx": 125}),
  "u4": ("act", U, 4, "Open a resource"),
  "s4": ("act", S, 4, "Open link in a new\nbrowser tab"),
  "d2": ("dec", U, 5, "Browse more?"),
  "en": ("end", U, 6, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","u2","r"), ("u2","r","s2","l"), ("s2","b","d1","t"), ("d1","r","s3","l", L("[quiz]")),
  ("d1","b","u4","t", L("[resource]")), ("u4","r","s4","l"), ("s4","b","d2","r"),
  ("d2","l","u2","l", {"label": "[yes]", "via": [((U, -150), None), (None, (2,))]}),
  ("d2","b","en","t", L("[no]")), ("s3","r","eq","l"),
])

D["manage_users"] = dict(title="Manage User", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open Users section"),
  "s1": ("act", S, 1, "Fetch all users\n(users collection)"),
  "a2": ("act", A, 2, "Search or filter,\nthen select a user"),
  "s2": ("act", S, 2, "Load profile, speeches\nand gamification record"),
  "a3": ("act", A, 3, "Edit details, change\nrole or delete account"),
  "s3": ("act", S, 3, "Ask for confirmation\nand validate"),
  "d1": ("dec", S, 4, "Valid and\nconfirmed?"),
  "s5": ("act", S, 5, "Update or delete the\nuser in Firestore"),
  "s6": ("act", S, 6, "Show success and\nrefresh the list"),
  "en": ("end", S, 7, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","a2","r"), ("a2","r","s2","l"), ("s2","b","a3","r"),
  ("a3","r","s3","l"), ("s3","b","d1","t"), ("d1","l","a3","b", L("[no] show error")),
  ("d1","b","s5","t", L("[yes]")), ("s5","b","s6","t"), ("s6","b","en","t"),
])

D["manage_gamification"] = dict(title="Manage Gamification Settings", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open Badges page or a\nuser's detail page"),
  "s1": ("act", S, 1, "Load badge definitions or\nthe user's gamification"),
  "a2": ("act", A, 2, "Edit badge (criteria, rarity,\nicon, active) or user XP\nand level", {"w": 230}),
  "a3": ("act", A, 3, "Save changes"),
  "s3": ("act", S, 3, "Validate inputs\n(numeric values)"),
  "d1": ("dec", S, 4, "Valid?"),
  "s5": ("act", S, 5, "Save to badgeDefinitions\nor userGamification"),
  "s6": ("act", S, 6, "Apply updated badge\nrules to all users"),
  "en": ("end", S, 7, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","a2","r"), ("a2","b","a3","t"), ("a3","r","s3","l"),
  ("s3","b","d1","t"),
  ("d1","l","a2","l", {"label": "[no] show error", "via": [((A, -150), None), (None, (2,))]}),
  ("d1","b","s5","t", L("[yes]")), ("s5","b","s6","t"), ("s6","b","en","t"),
])

D["session_history"] = dict(title="View Session History", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open History"),
  "s1": ("act", S, 1, "Retrieve speech history\n(Firestore)"),
  "d1": ("dec", S, 2, "Any sessions?"),
  "u2": ("act", U, 2, "See \"no sessions\nyet\" message"),
  "e1": ("end", U, 3, ""),
  "s3": ("act", S, 3, "List sessions with\ndate, type and scores"),
  "u4": ("act", U, 4, "Select a session"),
  "s4": ("act", S, 4, "Load full report: scores,\nfeedback, metrics, audio"),
  "u5": ("act", U, 5, "Review the details"),
  "d2": ("dec", U, 6, "View another?"),
  "en": ("end", U, 7, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","d1","t"), ("d1","l","u2","r", L("[no]")), ("u2","b","e1","t"),
  ("d1","b","s3","t", L("[yes]")), ("s3","b","u4","r"), ("u4","r","s4","l"), ("s4","b","u5","r"), ("u5","b","d2","t"),
  ("d2","l","u4","l", {"label": "[yes]", "via": [((U, -150), None), (None, (4,))]}),
  ("d2","b","en","t", L("[no]")),
])

D["view_badges"] = dict(title="View Badges / Achievements", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Badges"),
  "s1": ("act", S, 1, "Retrieve badge definitions\nand user progress"),
  "s2": ("act", S, 2, "Display badge grid"),
  "u3": ("act", U, 3, "Select a badge"),
  "s3": ("act", S, 3, "Show name, description,\ncriteria and rarity"),
  "d1": ("dec", S, 4, "Unlocked?"),
  "s5a": ("act", S, 5, "Show unlocked\nstyle and date", {"dx": -80, "w": 145}),
  "s5b": ("act", S, 5, "Show progress\nbar", {"dx": 85, "w": 135}),
  "u6": ("act", U, 6, "Close details"),
  "en": ("end", U, 7, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","s2","t"), ("s2","b","u3","r"), ("u3","r","s3","l"),
  ("s3","b","d1","t"), ("d1","l","s5a","t", L("[yes]")), ("d1","r","s5b","t", L("[no]")),
  ("s5a","b","u6","r"), ("s5b","b","u6","r"), ("u6","b","en","t"),
])

D["practice_mode"] = dict(title="Practice Mode", lanes=[U, S, B], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Open Practice Mode"),
  "s1": ("act", S, 1, "Load scripts and\nrecommended plan"),
  "u2": ("act", U, 2, "Select a script by\ncategory and difficulty"),
  "s2": ("act", S, 2, "Show reference script\nand target WPM"),
  "u3": ("act", U, 3, "Read the script aloud\nwhile recording"),
  "s3": ("act", S, 3, "Send recording"),
  "b3": ("act", B, 3, "Transcribe audio and\nextract acoustic features"),
  "s4": ("act", S, 4, "Compute word accuracy,\nmissed words and WPM"),
  "d1": ("dec", S, 5, "Speech found and\nmatches script?", {"w": 160}),
  "b6": ("act", B, 6, "Score delivery against\nthe script (RAG + LLM)"),
  "s7": ("act", S, 7, "Save practice session\n(pre/post scores)"),
  "u8": ("act", U, 8, "View accuracy, scores\nand coaching feedback"),
  "en": ("end", U, 9, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","u2","r"), ("u2","r","s2","l"), ("s2","b","u3","r"),
  ("u3","r","s3","l"), ("s3","r","b3","l"), ("b3","b","s4","r"), ("s4","b","d1","t"),
  ("d1","l","u3","b", L("[no] ask to retry")), ("d1","r","b6","t", L("[yes]")),
  ("b6","b","s7","r"), ("s7","b","u8","r"), ("u8","b","en","t"),
])

# ---------- new diagrams ----------
D["onboarding"] = dict(title="Complete Onboarding", lanes=[U, S], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Sign in for the\nfirst time"),
  "s1": ("act", S, 1, "Check profile in\nFirestore"),
  "d1": ("dec", S, 2, "Onboarding\ncomplete?"),
  "u2": ("act", U, 2, "Continue to\ndashboard"),
  "e1": ("end", U, 3, ""),
  "s3": ("act", S, 3, "Show onboarding steps"),
  "u4": ("act", U, 4, "Enter first name, last\nname, age and gender"),
  "u5": ("act", U, 5, "Choose interests and\ndefault speech type"),
  "u6": ("act", U, 6, "Tap Finish"),
  "s6": ("act", S, 6, "Save profile with\nonboardingComplete = true"),
  "s7": ("act", S, 7, "Open dashboard"),
  "en": ("end", S, 8, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","b","d1","t"), ("d1","l","u2","r", L("[yes]")), ("u2","b","e1","t"),
  ("d1","b","s3","t", L("[no]")), ("s3","b","u4","r"), ("u4","b","u5","t"), ("u5","b","u6","t"),
  ("u6","r","s6","l"), ("s6","b","s7","t"), ("s7","b","en","t"),
])

D["take_quiz"] = dict(title="Take Personalized Quiz", lanes=[U, S, B], nodes={
  "st": ("start", U, 0, ""),
  "u1": ("act", U, 1, "Choose a quiz category\n(speech type)"),
  "s1": ("act", S, 1, "Find weakest dimensions\nfrom session history"),
  "b1": ("act", B, 1, "Retrieve expert chunks\nfrom Corpus 2 (ChromaDB)"),
  "b2": ("act", B, 2, "Generate 10 questions\nfrom those chunks (LLM)"),
  "d1": ("dec", S, 3, "Quiz\ngenerated?"),
  "s4": ("act", S, 4, "Show questions\none at a time"),
  "u5": ("act", U, 5, "Answer a question"),
  "s5": ("act", S, 5, "Mark answer and show\nexplanation"),
  "d2": ("dec", U, 6, "More\nquestions?"),
  "s7": ("act", S, 7, "Show final score and\nsources"),
  "en": ("end", S, 8, ""),
}, edges=[
  ("st","b","u1","t"), ("u1","r","s1","l"), ("s1","r","b1","l"), ("b1","b","b2","t"), ("b2","b","d1","r"),
  ("d1","l","u1","b", L("[no] show error, retry")), ("d1","b","s4","t", L("[yes]")), ("s4","b","u5","r"),
  ("u5","r","s5","l"), ("s5","b","d2","r"),
  ("d2","l","u5","l", {"label": "[yes]", "via": [((U, -150), None), (None, (5,))]}),
  ("d2","b","s7","l", L("[no]")), ("s7","b","en","t"),
])

D["admin_login"] = dict(title="Admin Login", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open the admin app"),
  "s1": ("act", S, 1, "Show login form"),
  "a2": ("act", A, 2, "Enter email and\npassword"),
  "s2": ("act", S, 2, "Authenticate\n(Firebase Auth)"),
  "d1": ("dec", S, 3, "Valid?"),
  "d2": ("dec", S, 4, "role = admin?"),
  "a4": ("act", A, 4, "See \"access denied\"\nmessage"),
  "e1": ("end", A, 5, ""),
  "s5": ("act", S, 5, "Open admin dashboard"),
  "en": ("end", S, 6, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","a2","r"), ("a2","r","s2","l"), ("s2","b","d1","t"),
  ("d1","l","a2","b", L("[no] show error")), ("d1","b","d2","t", L("[yes]")), ("d2","l","a4","r", L("[no] sign out")),
  ("a4","b","e1","t"), ("d2","b","s5","t", L("[yes]")), ("s5","b","en","t"),
])

D["admin_dashboard"] = dict(title="View Admin Dashboard", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open Dashboard"),
  "s1": ("act", S, 1, "Load users, speeches and\ngamification records"),
  "d1": ("dec", S, 2, "Loaded?"),
  "a2": ("act", A, 2, "See permission\nerror message"),
  "e1": ("end", A, 3, ""),
  "s3": ("act", S, 3, "Compute totals: users,\nadmins, speeches, time,\naverage score"),
  "s4": ("act", S, 4, "Display statistics\ncards"),
  "a5": ("act", A, 5, "Review statistics"),
  "a6": ("act", A, 6, "Open Users, Speeches,\nBadges or Practice Mode"),
  "en": ("end", A, 7, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","d1","t"), ("d1","l","a2","r", L("[no]")), ("a2","b","e1","t"),
  ("d1","b","s3","t", L("[yes]")), ("s3","b","s4","t"), ("s4","b","a5","r"), ("a5","b","a6","t"), ("a6","b","en","t"),
])

D["monitor_speeches"] = dict(title="Monitor Speech Submissions", lanes=[A, S], nodes={
  "st": ("start", A, 0, ""),
  "a1": ("act", A, 1, "Open Speeches page"),
  "s1": ("act", S, 1, "Load every user's\nspeech history"),
  "s2": ("act", S, 2, "Display list and\nsummary statistics"),
  "a3": ("act", A, 3, "Filter by user, speech\ntype, date or score"),
  "s3": ("act", S, 3, "Apply filters and\nupdate statistics"),
  "d1": ("dec", A, 4, "Next step?"),
  "s5": ("act", S, 5, "Export filtered list\nas CSV"),
  "a5": ("act", A, 5, "Open the user's\ndetail page"),
  "en": ("end", A, 6, ""),
}, edges=[
  ("st","b","a1","t"), ("a1","r","s1","l"), ("s1","b","s2","t"), ("s2","b","a3","r"), ("a3","r","s3","l"),
  ("s3","b","d1","r"), ("d1","r","s5","t", L("[export]")), ("d1","b","a5","t", L("[view user]")),
  ("s5","b","en","r"), ("a5","b","en","t"),
])

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out, exist_ok=True)
    for k, spec in D.items():
        render(spec, os.path.join(out, f"act_{k}.svg"))
    print(len(D), "diagrams")
