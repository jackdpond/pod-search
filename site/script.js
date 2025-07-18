// Load seriesData from seriesData.json dynamically
fetch('seriesData.json')
  .then(response => response.json())
  .then(seriesData => {
    renderSidebar(seriesData);

    // Attach search functionality using the loaded data
    searchBtn.onclick = () => {
      const q = searchInput.value.trim();
      if (!q) {
        searchResults.innerHTML = '';
        return;
      }
      const results = searchEpisodes(q, seriesData);
      renderSearchResults(results);
    };

    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') searchBtn.onclick();
    });

    // Expose showEpisode globally for search results
    window.showEpisode = (series, episode) => showEpisode(series, episode);
  });

const seriesNav = document.getElementById('series-nav');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const searchResults = document.getElementById('search-results');

function renderSidebar(data) {
  seriesNav.innerHTML = '';
  Object.entries(data).forEach(([series, episodes], idx) => {
    const seriesDiv = document.createElement('div');
    seriesDiv.className = 'series';
    seriesDiv.textContent = series.replace(/_/g, ' ');
    seriesDiv.tabIndex = 0;
    seriesDiv.setAttribute('aria-expanded', 'false');

    const episodeList = document.createElement('ul');
    episodeList.className = 'episodes';
    episodeList.style.display = 'none';

    episodes.forEach(ep => {
      const epLi = document.createElement('li');
      epLi.className = 'episode';
      epLi.textContent = ep;
      epLi.tabIndex = 0;
      epLi.onclick = () => showEpisode(series, ep);
      episodeList.appendChild(epLi);
    });

    seriesDiv.onclick = () => {
      const expanded = seriesDiv.getAttribute('aria-expanded') === 'true';
      seriesDiv.setAttribute('aria-expanded', !expanded);
      episodeList.style.display = expanded ? 'none' : 'block';
    };

    seriesNav.appendChild(seriesDiv);
    seriesNav.appendChild(episodeList);
  });
}

function showEpisode(series, episode) {
  searchResults.innerHTML = `<div><strong>${series.replace(/_/g, ' ')}:</strong> ${episode}</div>`;
}

function searchEpisodes(query, data) {
  const results = [];
  Object.entries(data).forEach(([series, episodes]) => {
    episodes.forEach(ep => {
      if (ep.toLowerCase().includes(query.toLowerCase())) {
        results.push({ series, episode: ep });
      }
    });
  });
  return results;
}

function renderSearchResults(results) {
  if (results.length === 0) {
    searchResults.innerHTML = '<div>No results found.</div>';
    return;
  }
  searchResults.innerHTML = results.map(r =>
    `<div class="search-result" tabindex="0" onclick="showEpisode('${r.series}', '${r.episode.replace(/'/g, "\\'")}')">
      <strong>${r.series.replace(/_/g, ' ')}:</strong> ${r.episode}
    </div>`
  ).join('');
} 