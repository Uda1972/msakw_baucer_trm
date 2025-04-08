# Deploying Your Assistance Application System

This guide explains how to deploy your application for free on Render.com.

## Prerequisites

1. Create a free account on [Render.com](https://render.com/)
2. Have your project code in a GitHub repository (or ready to upload)

## Deployment Steps

### Option 1: Deploy from GitHub Repository

1. Log in to your Render.com account
2. Click on "New" and select "Web Service"
3. Connect your GitHub account and select your repository
4. Configure your service:
   - Name: `masjid-saidina-ali-assistance` (or your preferred name)
   - Runtime: Python 3
   - Build Command: `pip install -e .`
   - Start Command: `./deployment_start.sh`
5. Select "Free" plan
6. Click "Create Web Service"

Render will automatically detect the `render.yaml` file and use those settings.

### Option 2: Deploy using Render Dashboard

1. Log in to your Render.com account
2. Click "New" and select "Blueprint"
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file and suggest services to deploy
5. Review and click "Apply"

## Post-Deployment

After deployment:

1. Your application will be available at a URL like: `https://masjid-saidina-ali-assistance.onrender.com`
2. The database will be stored in a persistent disk
3. Free tier limitations:
   - The app will sleep after 15 minutes of inactivity
   - Limited to 750 hours of usage per month

## Keeping Your Application Active

For the free tier, the application will go to sleep after 15 minutes of inactivity. To keep it active:

1. Set up a monitoring service to ping your application regularly
2. You can use free services like UptimeRobot to send a ping every 5 minutes

## Database Considerations

The application uses SQLite, which on Render.com free tier will be stored in the application's ephemeral filesystem. This means:

1. **Data will persist between application deployments** (code updates)
2. **Data will be lost when the application is restarted** by Render.com after 15 minutes of inactivity

### Recommendations for Data Persistence

For more reliable data storage on the free tier, consider these options:

1. **Regular Backups**: Set up a scheduled task to download your database file regularly
2. **Keep Your App Active**: Use a service like UptimeRobot to ping your application every 10-15 minutes to prevent it from going inactive
3. **Upgrade to Paid Tier**: Render.com's paid tiers provide better persistence options
4. **External Storage**: If you have critical data, consider an external database service that has a free tier with better persistence guarantees (like Supabase, Neon, or Railway)

### Backup Instructions 

To manually back up your database:
1. Log in to Render.com
2. Go to your web service
3. Open the Shell tab
4. Run the command: `cp /path/to/app.db /tmp/backup.db`
5. Download the file using Render's file browser

## Troubleshooting

If you encounter issues:

1. Check the logs in the Render dashboard
2. Ensure all environment variables are properly set
3. Verify the build and start commands are correct

Remember that the free tier has limited resources, so optimize your application accordingly.