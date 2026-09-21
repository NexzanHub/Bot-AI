import discord
from discord.ext import commands
from discord import app_commands

# Ganti dengan Token Bot terbaru dari Developer Portal
TOKEN = "MTU1MDQ3NDM4MzI5Mjc2NDE5Mg.GoOD12.wqZUuBy7OIy_T64wsQWVRB23y4pfYqnsKyxHlE"

# ID Pemilik Bot / Admin Nexzan Hub
ALLOWED_USER_ID = 1404811419786018837

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

bot = Client()

# Tombol Get Script (Ephemeral/Hanya bisa dilihat yang klik)
class ScriptButton(discord.ui.Button):
    def __init__(self, loadstring: str):
        super().__init__(
            label="Get Script",
            style=discord.ButtonStyle.primary,
            emoji="📜"
        )
        self.loadstring = loadstring

    async def callback(self, interaction: discord.Interaction):
        # Mencegah timeout / Application Did Not Respond
        await interaction.response.defer(ephemeral=True)

        mobile_format = f"`{self.loadstring}`"
        pc_format = f"```lua\n{self.loadstring}\n```"

        response_content = (
            "### 🚀 **Nexzan Hub - Script Loader**\n"
            "Gunakan script di bawah sesuai dengan perangkat yang kamu gunakan:\n\n"
            f"📱 **Mobile Version (Klik/Tap untuk salin):**\n{mobile_format}\n\n"
            f"💻 **PC Version:**\n{pc_format}"
        )

        await interaction.followup.send(response_content, ephemeral=True)

class GetScriptView(discord.ui.View):
    def __init__(self, loadstring: str):
        super().__init__(timeout=None)
        self.add_item(ScriptButton(loadstring))

# Modal Form Pengumuman
class AnnouncementModal(discord.ui.Modal):
    def __init__(self, announcement_type: str):
        super().__init__(title="Buat Pengumuman Script")
        self.announcement_type = announcement_type

    map_name = discord.ui.TextInput(
        label="Nama Map / Game",
        placeholder="Contoh: Blox Fruits",
        required=True
    )

    feature_list = discord.ui.TextInput(
        label="Fitur List",
        style=discord.TextStyle.paragraph,
        placeholder="• Auto Farm\n• Auto Quest\n• Teleport",
        required=True
    )

    loadstring_input = discord.ui.TextInput(
        label="Loadstring Script",
        style=discord.TextStyle.paragraph,
        placeholder="loadstring(game:HttpGet('...'))()",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Tahan respon seketika
        await interaction.response.defer(ephemeral=True)

        try:
            if self.announcement_type == "release":
                title = "🎉 NEXZAN HUB RELEASE SCRIPT"
                color = discord.Color.green()
            else:
                title = "⚡ NEXZAN UPDATE SCRIPT"
                color = discord.Color.blue()

            embed = discord.Embed(
                title=title,
                color=color
            )
            embed.add_field(name="🎮 Nama Map", value=self.map_name.value, inline=False)
            embed.add_field(name="📋 Fitur List", value=self.feature_list.value, inline=False)
            embed.set_footer(text="Nexzan Hub • Klik tombol di bawah untuk mengambil script!")

            view = GetScriptView(loadstring=self.loadstring_input.value)

            # Kirim pengumuman ke channel
            await interaction.channel.send(embed=embed, view=view)

            # Konfirmasi sukses ke pengguna
            await interaction.followup.send("✅ Pengumuman berhasil dikirim ke channel!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Terjadi kesalahan: {e}", ephemeral=True)

# Perintah Slash /announce
@bot.tree.command(name="announce", description="Kirim pengumuman script baru ke channel (Khusus Owner)")
@app_commands.choices(tipe=[
    app_commands.Choice(name="Nexzan Hub Release Script", value="release"),
    app_commands.Choice(name="Nexzan Update Script", value="update")
])
async def announce(interaction: discord.Interaction, tipe: app_commands.Choice[str]):
    if interaction.user.id != ALLOWED_USER_ID:
        await interaction.response.send_message("❌ Perintah ini khusus untuk Owner Nexzan Hub!", ephemeral=True)
        return

    await interaction.response.send_modal(AnnouncementModal(tipe.value))

# Perintah manual sync slash command
@bot.command()
async def sync(ctx):
    if ctx.author.id == ALLOWED_USER_ID:
        await bot.tree.sync()
        await ctx.send("✅ Slash command berhasil di-sync!")

@bot.event
async def on_ready():
    print(f"Bot berhasil online sebagai: {bot.user}")

bot.run(TOKEN)
