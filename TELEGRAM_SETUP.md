# Telegram Bot Setup Guide

## Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather
3. **Send the command**: `/newbot`
4. **Follow the prompts**:
   - Enter a name for your bot (e.g., "Daily Scraper Notifications")
   - Enter a username for your bot (must end with 'bot', e.g., "my_scraper_bot")
5. **Save the bot token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your Chat ID

### Method 1: Using @userinfobot (Easiest)
1. **Search for `@userinfobot`** in Telegram
2. **Start a chat** with it
3. **Send any message** to it
4. **It will reply** with your chat ID (a number like `123456789`)

### Method 2: Using your bot
1. **Start a chat** with your bot (search for the username you created)
2. **Send any message** to your bot
3. **Visit this URL** in your browser (replace with your bot token):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. **Look for the "chat" object** and find your `id` number

## Step 3: Add Secrets to GitHub

1. **Go to your GitHub repository**
2. **Click Settings** → **Secrets and variables** → **Actions**
3. **Add these two secrets**:

   **Secret 1:**
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token from Step 1

   **Secret 2:**
   - **Name**: `TELEGRAM_CHAT_ID`
   - **Value**: Your chat ID from Step 2

## Step 4: Test Your Setup

1. **Go to your repository's Actions tab**
2. **Find the "Daily Scraper" workflow**
3. **Click "Run workflow"** → **"Run workflow"**
4. **Check your Telegram** for the notification

## Troubleshooting

### Bot not responding?
- Make sure you've started a chat with your bot
- Check that your bot token is correct
- Verify your chat ID is correct

### Getting "Forbidden" error?
- Make sure you've sent at least one message to your bot
- Check that your chat ID is correct

### Message not formatted properly?
- The bot uses HTML formatting
- Make sure the `changes.md` file doesn't contain special characters that break the JSON

## Advantages of Telegram

✅ **Mobile-first**: Perfect for phone notifications  
✅ **Private**: Only you receive the messages  
✅ **No server needed**: Direct bot-to-user communication  
✅ **Rich formatting**: Supports HTML, files, images  
✅ **Reliable**: Telegram's API is very stable  
✅ **Free**: No cost involved  

## Optional: Create a Channel

If you want to share notifications with others:

1. **Create a Telegram channel**
2. **Add your bot as an admin** to the channel
3. **Get the channel ID** (usually starts with `-100`)
4. **Use the channel ID** as your `TELEGRAM_CHAT_ID`

## What You'll Receive

The notification will include:
- 🔄 **Bold title** indicating it's a scraper update
- 📄 **Formatted content** from your `changes.md` file
- 📅 **Timestamp** of when the scrape occurred
- 💬 **Clean formatting** with proper code blocks

The notification will only be sent when there are actual changes to report! 