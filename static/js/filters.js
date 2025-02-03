document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter-btn");
    const clearFiltersButton = document.getElementById("clear-filters");
    const citiesContainer = document.querySelector(".cities-container");

    function applyFilters() {
        const selectedColors = Array.from(filterButtons)
            .filter(btn => btn.getAttribute("data-selected") === "true")
            .map(btn => btn.getAttribute("data-color").toLowerCase());

        // Envia as cores selecionadas para o backend
        fetch(`/cities/filter/?colors=${selectedColors.join('&colors=')}`)
            .then(response => response.json())
            .then(data => {
                // Limpa o container de cidades
                citiesContainer.innerHTML = '';

                // Adiciona as cidades filtradas ao container
                data.cities.forEach(city => {
                    const cityCard = document.createElement('div');
                    cityCard.className = 'city-card';
                    cityCard.setAttribute('data-colors', city.colors);

                    cityCard.innerHTML = `
                        ${city.image_url ? `<img src="${city.image_url}" alt="${city.name}">` : '<div class="no-image">Sem imagem</div>'}
                        <h3>${city.name}</h3>
                        <p>Rarity: #${city.description}</p>
                    `;

                    citiesContainer.appendChild(cityCard);
                });
            })
            .catch(error => console.error('Erro ao filtrar cidades:', error));
    }

    filterButtons.forEach(button => {
        button.addEventListener("click", function () {
            const selected = this.getAttribute("data-selected") === "true";
            this.setAttribute("data-selected", !selected);
            applyFilters();
        });
    });

    clearFiltersButton.addEventListener("click", function () {
        filterButtons.forEach(btn => btn.removeAttribute("data-selected"));
        applyFilters();
    });

    applyFilters();
});