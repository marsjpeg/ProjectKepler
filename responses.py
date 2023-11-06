import random
import discord

#non-embedded responses vvvvv
def get_response(message: str) -> str:
    p_message = message.lower()
    #commands
    if p_message == "k!roll":
        return str(random.randint(1,6))
    
    if message.startswith('k!8ball'):
        replies = ["Most Definetely!", "No.", "Yes.", "Reply Hazy, Try Again.", "Maybe...", "Definetely Not.", "Not Sure.", "Not A Great Outcome."]
        index = random.randint(0,7)
        return replies[index]
    
    if p_message == "k!fortune":
        fortune = ["A beautiful, smart, and loving person will be coming into your life.", "A dubious friend may be an enemy in camouflage.", "A faithful friend is a strong defense.", "A feather in the hand is better than a bird in the air.", "A golden egg of opportunity falls into your lap this month.", "A gambler not only will lose what he has, but also will lose what he doesn’t have.", "All your hard work will soon pay off.", "Advice, when most needed, is least heeded.", "An inch of time is an inch of gold.", "Do not demand for someone’s soul if you already got his heart.", "Do not let ambitions overshadow small success.", "Do not make extra work for yourself.", "Do not underestimate yourself. Human beings have unlimited potentials.", "Fortune Not Found: Abort, Retry, Ignore?", "From listening comes wisdom and from speaking repentance.", "From now on your kindness will lead you to success.", "Get your mind set – confidence will lead you on."]
        answer = random.choice(fortune)
        return answer
    
    if p_message[:2] == "k!":
        return "I didn't get that. Try looking at 'k!help' for commands!"