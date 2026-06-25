// Cápsula de Estudos — script.js

console.log("Cápsula de Estudos carregada.");

// ---------- alternar tema claro/escuro ----------

(function () {
  const botaoTema = document.getElementById("theme-toggle");
  const iconeSol = document.getElementById("icon-sun");
  const iconeLua = document.getElementById("icon-moon");

  if (!botaoTema) return;

  function atualizarIcone() {
    const temaAtual = document.documentElement.getAttribute("data-theme");
    const ehEscuro = temaAtual === "dark";

    iconeSol.style.display = ehEscuro ? "block" : "none";
    iconeLua.style.display = ehEscuro ? "none" : "block";
  }

  atualizarIcone();

  botaoTema.addEventListener("click", function () {
    const temaAtual = document.documentElement.getAttribute("data-theme");
    const novoTema = temaAtual === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", novoTema);
    localStorage.setItem("tema", novoTema);
    atualizarIcone();
  });
})();
