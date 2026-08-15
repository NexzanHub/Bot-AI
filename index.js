const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder } = require("discord.js");

const token = process.env.DISCORD_TOKEN;
const clientId = process.env.CLIENT_ID;

if (!token) {
  console.error("DISCORD_TOKEN belum diatur di Environment Variables.");
  process.exit(1);
}

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

const commands = [
  new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Cek apakah bot aktif."),
  new SlashCommandBuilder()
    .setName("status")
    .setDescription("Lihat status bot.")
].map(command => command.toJSON());

client.once("ready", async () => {
  console.log(`Bot online sebagai ${client.user.tag}`);

  // Jika CLIENT_ID diisi, daftarkan slash commands secara global.
  if (clientId) {
    try {
      const rest = new REST({ version: "10" }).setToken(token);
      await rest.put(
        Routes.applicationCommands(clientId),
        { body: commands }
      );
      console.log("Slash commands berhasil didaftarkan.");
    } catch (error) {
      console.error("Gagal mendaftarkan slash commands:", error);
    }
  }
});

client.on("interactionCreate", async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === "ping") {
    await interaction.reply(`🏓 Pong! Latency: ${client.ws.ping}ms`);
  }

  if (interaction.commandName === "status") {
    await interaction.reply("🟢 Nexzan Hub Bot sedang online.");
  }
});

client.login(token);
