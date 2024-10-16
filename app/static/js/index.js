const pokemon_container = document.querySelector(".card-container");
const form = document.querySelector("form");
const input = document.querySelector("input");
const searchButton = document.querySelector(".searchIcon");
const checkboxInput = document.querySelector('input[type="checkbox"]');

// URLs dos ícones de Pokébola, fornecidos pelo template HTML
const pokeballIcon = document.querySelector("#pokeballIcon").dataset.url;
const pokeballFillIcon =
  document.querySelector("#pokeballFillIcon").dataset.url;

checkboxInput.addEventListener("change", checkCheckboxStatus);
searchButton.addEventListener("click", searchPokemon);
form.addEventListener("submit", function (event) {
  event.preventDefault();
  searchPokemon();
});

isAuthenticated = localStorage.getItem("User") ? true : false;

async function getAllPokemon() {
  try {
    if (isAuthenticated) {
      const user = localStorage.getItem("User");
      // Se o usuário está autenticado, traz apenas os Pokémons capturados
      const response = await fetch(`/api/capturados?user=${user}`);
      if (!response.ok) throw new Error("Erro ao buscar Pokémons capturados");

      pokemons = await response.json();
    } else {
      // Se o usuário não está autenticado, traz todos os Pokémons
      const response = await fetch("/api/pokemons");
      if (!response.ok) throw new Error("Erro ao buscar todos os Pokémons");

      pokemons = await response.json();
    }

    // Renderiza os cards de Pokémon
    pokemons.forEach((poke) => renderCard(poke));
    console.log(pokemons);
  } catch (error) {
    console.error(error);
    alert("Não foi possível carregar os Pokémons.");
  }
}

window.onload = function () {
  getAllPokemon();
};

async function captureButtonPressed(event, id_pokemon) {
  if (isAuthenticated) {
    const user = localStorage.getItem("User");
    try {
      if (event.target.src.includes(pokeballIcon)) {
        // aqui ele será favoritado
        event.target.src = pokeballFillIcon;
        const response = await fetch(
          `/api/add_captura?user=${user}&id_pokemon=${id_pokemon}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao capturar pokemon");
      } else {
        // aqui ele será desfavoritado
        event.target.src = pokeballIcon;
        const response = await fetch(
          `/api/remove_captura?user=${user}&id_pokemon=${id_pokemon}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) throw new Error("Erro ao remover captura");
      }
    } catch (error) {
      console.error(error);
      alert(error);
    }
  } else {
    alert("Necessário estar logado para capturar pokemon");
  }
}

function checkCheckboxStatus() {
  return;
}

async function searchPokemon() {
  const pesquisa = input.value;
  clearPokemon();
  if (pesquisa != "") {
    try {
      const response = await fetch(`/api/pesquisar_pokemon?search=${pesquisa}`);
      if (!response.ok) throw new Error("Erro ao buscar Pokémons");

      pokemons = await response.json();

      // Renderiza os cards de Pokémon
      pokemons.forEach((poke) => renderCard(poke));
      console.log(pokemons);
    } catch (error) {
      console.error(error);
      alert(error);
    }
    // Se o usuário está autenticado, traz apenas os Pokémons capturados
  } else {
    getAllPokemon();
  }
  return;
}

function renderCard(pokemon) {
  const cardContainer = document.querySelector(".card-container"); // Selecione o contêiner onde os cards serão renderizados

  const card = document.createElement("div");
  card.classList.add("card");

  // Criação do contêiner da imagem
  const imageContainer = document.createElement("div");
  imageContainer.classList.add("image-container");

  // Imagem do Pokémon
  const pokemonImage = document.createElement("img");
  pokemonImage.src = pokemon.url_image;
  pokemonImage.alt = pokemon.nome;
  pokemonImage.classList.add("pokemon-image");

  // Ícone de captura
  const captureIcon = document.createElement("img");
  captureIcon.src = pokemon.capturado ? pokeballFillIcon : pokeballIcon;
  captureIcon.alt = "Capture Icon";
  captureIcon.classList.add("capture-icon");
  captureIcon.addEventListener("click", (event) =>
    captureButtonPressed(event, pokemon.id)
  );

  // Adiciona as imagens ao contêiner da imagem
  imageContainer.appendChild(pokemonImage);
  imageContainer.appendChild(captureIcon);

  // Adiciona o contêiner da imagem ao card
  card.appendChild(imageContainer);

  // Adiciona o número do Pokémon
  const pokemonNumber = document.createElement("p");
  pokemonNumber.classList.add("pokemon-number");
  pokemonNumber.textContent = `Nº ${("000" + pokemon.id).slice(-4)}`;
  card.appendChild(pokemonNumber);

  // Adiciona o nome do Pokémon
  const pokemonName = document.createElement("h2");
  pokemonName.textContent = pokemon.nome;
  card.appendChild(pokemonName);

  // Criação da seção de tipos
  const pokemonTypes = document.createElement("div");
  pokemonTypes.classList.add("pokemon-types");

  const baseType = document.createElement("span");
  baseType.classList.add("type", "type-base");
  baseType.textContent = pokemon.tipo_base;

  pokemonTypes.appendChild(baseType);

  if (pokemon.tipo_sec) {
    const secondaryType = document.createElement("span");
    secondaryType.classList.add("type", "type-secondary");
    secondaryType.textContent = pokemon.tipo_sec;
    pokemonTypes.appendChild(secondaryType);
  }

  card.appendChild(pokemonTypes); // Adiciona a seção de tipos ao card
  cardContainer.appendChild(card); // Adiciona o card ao contêiner
}

function clearPokemon() {
  pokemon_container.innerHTML = "";
}
