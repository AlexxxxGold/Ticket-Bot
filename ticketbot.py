import discord
from discord.ext import commands
from discord.ui import View, Select

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(View):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.category1 = None

        self.add_item(Select(
            placeholder="Choose the first category",
            options=[
                discord.SelectOption(label="Category 1", value="1"),
                discord.SelectOption(label="Category 2", value="2"),
                discord.SelectOption(label="Category 3", value="3")
            ],
            custom_id="category1"
        ))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.user

    @discord.ui.select.callback
    async def category1_selected(self, select, interaction: discord.Interaction):
        self.category1 = select.values[0]
        view = SubCategoryView(self.user, self.category1)
        await interaction.response.send_message("Choose the second category:", view=view, ephemeral=True)

class SubCategoryView(View):
    def __init__(self, user, category1):
        super().__init__()
        self.user = user
        self.category1 = category1

        self.add_item(Select(
            placeholder="Choose the second category",
            options=[
                discord.SelectOption(label="Category 1", value="1"),
                discord.SelectOption(label="Category 2", value="2"),
                discord.SelectOption(label="Category 3", value="3")
            ],
            custom_id="category2"
        ))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.user

    @discord.ui.select.callback
    async def category2_selected(self, select, interaction: discord.Interaction):
        category2 = select.values[0]
        channel_name = f"{self.category1}{category2}"
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            self.user: discord.PermissionOverwrite(read_messages=True),
            discord.utils.get(guild.roles, name=f"Role-{self.category1}{category2}"): discord.PermissionOverwrite(read_messages=True),
        }
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ticket(ctx):
    view = TicketView(ctx.author)
    await ctx.send("Choose the first category:", view=view)

bot.run("MTMyMjEwMTM3MjczNjI0MTc2NA.GYSuGv.GOcvni9OdYGsCm9mQgWmuxUjXQ4dHo8aZSn1fM")
