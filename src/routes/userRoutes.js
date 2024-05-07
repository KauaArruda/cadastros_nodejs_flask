const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");

// Rotas de Usuários
router.get("/", userController.getAllUsers);
router.post("/", userController.createUser);
router.put("/:id", userController.updateUser);
router.delete("/:id", userController.deleteUser);

module.exports = router;
