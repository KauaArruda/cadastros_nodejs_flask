// Adiciona um ouvinte de evento ao formulário de login para processar a submissão
document.getElementById("form_login").addEventListener("submit", async function (e) {
  e.preventDefault(); // Impede o envio padrão do formulário

  // Recupera os valores de e-mail e senha do formulário
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  // Tenta fazer uma solicitação de login para o servidor
  try {
    const response = await fetch("http://localhost:3000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });

    if (response.ok) {
      const data = await response.json(); // Converte a resposta em JSON
      console.log("Seu login foi realizado com sucesso!", data);
      // Redireciona o usuário para a página inicial após o login bem-sucedido
      window.location.href = "http://127.0.0.1:5000/";
    } else {
      // Caso o servidor responda com um status de erro, lança uma exceção
      const errorData = await response.json(); // Assume que o servidor envia uma mensagem de erro em JSON
      throw new Error(`Falha na requisição: ${errorData.message}`);
    }
  } catch (error) {
    // Mostra um erro no console e fornece feedback ao usuário
    console.error("Erro ao fazer a requisição:", error);
    alert("Erro ao tentar fazer login: " + error.message); // Alerta o usuário sobre o erro
  }
});
