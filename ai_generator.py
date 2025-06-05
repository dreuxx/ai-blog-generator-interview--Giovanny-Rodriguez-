import os
import openai
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.warning("OpenAI API key not found. Using mock mode.")
            self.mock_mode = True
        else:
            openai.api_key = self.api_key
            self.mock_mode = False
            
        self.affiliate_links = [
            "{{AFF_LINK_1}}",
            "{{AFF_LINK_2}}",
            "{{AFF_LINK_3}}"
        ]
    
    def generate_post(self, keyword: str, seo_metrics: Dict[str, Any]) -> str:
        logger.info(f"Generating blog post for: {keyword}")
        
        if self.mock_mode:
            return self._generate_mock_post(keyword, seo_metrics)
        else:
            return self._generate_ai_post(keyword, seo_metrics)
    
    def _create_prompt(self, keyword: str, seo_metrics: Dict[str, Any]) -> str:
        # TU PROMPT PERSONALIZADO
        return f"""
        Hey there! 👋 Could you help me create an awesome guide about "{keyword}"? 
        Imagine you're explaining it to a friend over coffee - warm, helpful, and packed with real value.

        Here's what we're working with:
        🔍 Monthly searches: {seo_metrics['search_volume']} people looking for this
        📊 Difficulty level: {seo_metrics['keyword_difficulty']}/100
        🥊 Competition: {seo_metrics['competition']}
        ✨ Related terms: {', '.join(seo_metrics['related_keywords'][:5])} (and others)

        Here's how we'd love the post to feel:

        1. Start with a catchy title featuring "{keyword}"
        2. Open with a warm intro (100-150 words) that makes readers think "Yes, this is for me!"
        3. Build 3-5 main sections (200-300 words each) with clear headings
        4. Naturally weave "{keyword}" into the flow 3-5 times - no stuffing!
        5. Sprinkle related keywords like "{seo_metrics['related_keywords'][0]}" where they fit naturally
        6. Wrap up with motivation to take action
        7. Place affiliate markers where helpful: {{{{AFF_LINK_1}}}}, {{{{AFF_LINK_2}}}}, {{{{AFF_LINK_3}}}}
        8. Use Markdown formatting for readability

        Most importantly: Write like a human who genuinely cares. Focus on:
        - Solving real problems
        - Sharing "aha!" moments
        - Making complex ideas simple
        - Keeping the tone warm and conversational

        For structure inspiration:
        [Title that grabs attention]
        [Intro that connects emotionally]
        [Helpful section 1]
        [Practical section 2]
        [Solution-focused section 3]
        [Encouraging conclusion]

        We trust your wisdom! Create something that would make readers say:
        "This finally makes sense - and I feel ready to try it!"
        """
    
    def _generate_ai_post(self, keyword: str, seo_metrics: Dict[str, Any]) -> str:
        try:
            writing_guide = self._create_prompt(keyword, seo_metrics)
            
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You're a skilled writer who makes complex topics feel like friendly conversations"
                    },
                    {
                        "role": "user", 
                        "content": writing_guide
                    }
                ],
                max_tokens=2000,
                temperature=0.7,
                top_p=0.9
            )
            
            fresh_content = chat.choices[0].message['content']
            post_header = self._create_metadata(keyword, seo_metrics)
            return f"{post_header}\n\n{fresh_content}"
            
        except Exception as e:
            logger.warning(f"AI took a coffee break ☕️ | Problem: {str(e)}")
            logger.info("Switching to our trusty backup writer...")
            return self._generate_mock_post(keyword, seo_metrics)
    
    def _generate_mock_post(self, keyword: str, seo_metrics: Dict[str, Any]) -> str:
        metadata = self._create_metadata(keyword, seo_metrics)
        
        # TU TEMPLATE PERSONALIZADO
        content = f"""# Your Friendly Guide to {keyword.title()}: Everything You Need to Know

## Let's Talk About {keyword.title()} Together!

Hey there! 👋 So you're curious about {keyword}? You're in good company! Whether you're just dipping your toes in or you've been exploring this space for a while, this guide is like having coffee with a friend who's been where you are. I'll share what I've learned, what actually works, and how you can start seeing real results.

Fun fact: Every month, {seo_metrics['search_volume']:,} people search for this exact topic - and with {seo_metrics['competition']} competition, standing out matters. Let's cut through the noise together!

## So... What Exactly is {keyword.title()}?

Okay, real talk: {keyword} can seem overwhelming at first. But strip away the jargon, and it's really about connecting dots in a new way. 

Most folks get tripped up because:
- They try to learn everything at once
- They get lost in theory without practice
- They don't have a clear roadmap (that's where we come in!)

**The good news?** You don't need to be an expert overnight. We'll take this step by step. 

👉 Friendly tip: This [starter resource]({self.affiliate_links[0]}) helped me when I was beginning

## Why Bother with {keyword.title()}? (Spoiler: It's Worth It!)

Here's why I think {keyword} is genuinely exciting:

1. **It's changing industries**  
   Companies are hungry for people who get this stuff - it's becoming a superpower!

2. **It changes how you see things**  
   Learning this shifted my perspective in ways I never expected - both at work and in daily life.

3. **You'll use it more than you think**  
   From practical applications to creative solutions, these skills pop up everywhere!

{self.affiliate_links[1]} has awesome tools that make the journey easier

## Your Stress-Free Starting Point

Breathe! Starting is simpler than you think:

### Step 1: Lay your foundation
Don't build a house on sand! Focus on:
- The 2-3 core ideas that matter most
- What terms actually mean (not just textbook definitions)
- What "good" looks like in practice

### Step 2: Make it a habit, not homework
Just 15 minutes daily beats 5 hours monthly. Try:
- Tiny daily experiments
- Journaling what works
- Celebrating small wins!

### Step 3: Find your guides
Connect with people who've been there! I learned tons from:
- Industry newsletters on the topic
- This surprisingly practical [workshop]({self.affiliate_links[2]})
- Local meetups (yes, they still exist!)

## Hurdles You Might Face (And How to Leap Over Them)

We all hit bumps! Here's how I navigated:

**"There's too much information!"**  
→ *Try this:* Pick ONE trusted source. Ignore everything else for 30 days.

**"I feel like I'm just faking it"**  
→ *Try this:* Create something small but real - even if it's just for you.

**"Things change too fast!"**  
→ *Try this:* Follow 2-3 trusted voices - they filter the noise beautifully.

## When You're Ready to Level Up

Once you're comfy with basics, try these power moves:
- Mix methods like a chef experiments with flavors
- Teach someone else (you'll learn more than they do!)
- Build your "lessons learned" notebook

P.S. You might also love: {', '.join(seo_metrics['related_keywords'][:3])}

## Wrapping It Up With Heart

Look - mastering {keyword} isn't about perfection. It's about showing up, staying curious, and applying what you learn. Some days you'll feel like a rockstar, others you'll question everything. Both are part of the journey!

**Your next step?** Pick ONE thing from this guide and try it today. Then hit reply and tell me how it went - I'd genuinely love to hear!

---

*Guide gently updated on {datetime.now().strftime('%B %d, %Y')} over a virtual coffee ☕*"""
        
        return metadata + "\n\n" + content
    
    def _create_metadata(self, keyword: str, seo_metrics: Dict[str, Any]) -> str:
        human_date = datetime.now().strftime('%B %d, %Y')
        
        return f"""---
# Your Friendly Guide to {keyword.title()}
# Created with care on {human_date}
#
# Behind the scenes:
#   - Every month, {seo_metrics['search_volume']:,} people search for this
#   - It's considered a {seo_metrics['keyword_difficulty']}/100 in difficulty
#   - Competition level: {seo_metrics['competition']}

focus_keyword: "{keyword}"
guide_created: {datetime.now().isoformat()}
---"""