# GenAI // Labbyta

### Vad?
Det här är en labbyta som du snabbt kan sätta upp lokalt eller exempelvis på [Streamlit](https://streamlit.io/), för att låta användare prova generativa AI-verktyg utan att behöva skapa egna konton.  
Det enda som behövs är en API-nyckel från OpenAI.  
Den här labbytan är en del av den utbildningsmiljö som jag använder och sätter upp inför exempelvis 
workshops, masterclasses och annat.


![Bild som visar labbytan](images/preview.jpg)

### AI-verktyg?
Just nu finns det följande verktyg:
- Chat // Chatta med en språkmodell, som GPT-4o från OpenAI eller om du har API från Groq även LLama
- Bild // Generera bilder med DALL-E 3 från OpenAI
- Bildanalys // Analysera bilder med GPT-4o från OpenAI
- Chat med dokument // Enkel RAG för att kunna ladda upp ett eller flera dokument som du kan chatta med
- Transkribering // Spela in din röst direkt via webbläsaren eller ladda upp ljudfil, så får du den transkriberad till text med Whisper från OpenAI

Du kan tänka på det som ett uppstyckat ChatGPT, där de olika delarna är uppdelade i separata tjänster.

## Installation

### Du behöver
Miljön är kodad i Python med öppen mjukvara, så det finns inga kostnader kopplat till det. Konto på GitHub och Streamlit är också kostnadsfritt.  
Dock behöver du en API-nyckel från OpenAI för att kunna använda deras tjänster. API-nyckeln har 
ingenting att göra med ChatGPT, utan är helt separat. Gällande betalning, så sätter man in pengar 
i förväg och kostnad beräknas på användande.  

- API-nyckel skaffar du på [platform.openai.com](https://platform.openai.com/)
- Konto på  - För att kunna skapa en kopia av koden om du vill köra den online på Streamlit
- Konto på Streamlit  - Här kommer du att drifta din labbyta

### Installation på Streamlit
Se film
1. Skapa konto på [GitHub](https://github.com/)
2. Skapa konto på Streamlit - [share.streamlit.io](https://share.streamlit.io/) - genom att logga in med ditt GitHub-konto. Då kopplas dina konton ihop automatiskt.
3. Gå till https://github.com/mickekring/gen-ai-labb och klicka på "Fork", så klonas koden till din GitHub.
4. Gå till [share.streamlit.io](https://share.streamlit.io/) och klicka på "Create App"
5. Välj "Deploy from a public app from GitHub"
6. I "Repository", välj den som heter "gen-ai-lab".
7. "Branch" ska stå på "main".
8. I "Main file path" väljer du "Start.py"
9. Vid "App URL" väljer du det domännamn du vill ha till din labbyta, som exempelvis "mittlabb". Då blir adressen mittlabb.streamlit.app 
10. Klicka på "Advanced settings" och klistra in nedanstående. Inom citationstecknen så klistrar du in din API-nyckel till OpenAI och istället för "password123" så sätter du ett eget lösenord för att komma åt sidan. Om du ändrar "pwd_on" till false så krävs inget lösenord för att komma åt sidan.

openai_key = ""  
pwd_on = "true"  
password = "password123"  




