const express = require("express");
//Importando dotenv para usar variaveis de ambiente
require("dotenv").config();
//importando as rotas
const userRoutes = require("../src/routes/userRoutes");

const mongoose = require("mongoose");

//Importando banco de dados
const ConnectMongoDB = require("../src/database");

//Instanciando express para recerber  as funções do framework
const app = express();

//Garante interação entre dominios diferentes
const cors = require("cors");

const User = require("../src/models/user");

//Conectando ao banco de dados
ConnectMongoDB();

app.use(express.json());
app.use("/api/users", userRoutes);
app.use(cors());

app.post("/api/login", async (req, res) => {
  const { email, senha } = req.body;

  try {
    const user = await User.findOne({ email, senha });

    if (!user) {
      return res.status(401).json({ message: "Login inválido" });
    }

    return res.status(200).json({ message: "Logado com sucesso!" });
  } catch (error) {
    console.error("Erro ao logar:", error);
    res.status(500).json({ message: "Erro no servidor" });
  }
});

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

const server = app.listen(process.env.PORT || 3000, () => {
  const { address, port } = server.address();
  const hostname = address === "::" ? "localhost" : address;
  console.log(`Server rodando na porta:http://${hostname}:${port}/`);
});

console.log(process.env.MONGODB_URI);
console.log(process.env.PORT);
