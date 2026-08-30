const API_BASE_URL = "http://127.0.0.1:8000";

/*
|--------------------------------------------------------------------------
| Generic API helper
|--------------------------------------------------------------------------
*/

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      `Server returned an invalid response (${response.status}).`
    );
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
        data?.message ||
        `Request failed with status ${response.status}.`
    );
  }

  return data;
}

/*
|--------------------------------------------------------------------------
| Health
|--------------------------------------------------------------------------
*/

export async function checkBackend() {
  return request("/health");
}

/*
|--------------------------------------------------------------------------
| Climate / Weather
|--------------------------------------------------------------------------
|
| Current backend expects:
| state
| district
| crop
| village (optional)
|--------------------------------------------------------------------------
*/

export async function getWeather({
  state,
  district,
  crop,
  village = "",
}) {
  const params = new URLSearchParams();

  params.append("state", state);
  params.append("district", district);
  params.append("crop", crop);

  if (village.trim()) {
    params.append("village", village);
  }

  return request(
    `/weather?${params.toString()}`
  );
}

/*
|--------------------------------------------------------------------------
| Crop Planning
|--------------------------------------------------------------------------
*/

export async function getCropRecommendations({
  city,
  soil_ph,
}) {
  return request("/crop/recommend", {
    method: "POST",

    body: JSON.stringify({
      city,
      soil_ph,
    }),
  });
}

/*
|--------------------------------------------------------------------------
| Market
|--------------------------------------------------------------------------
*/

export async function getMarketAnalysis({
  crop,
  state,
  district,
}) {
  return request("/market/analyze", {
    method: "POST",

    body: JSON.stringify({
      crop,
      state,
      district,
    }),
  });
}

/*
|--------------------------------------------------------------------------
| Government Schemes
|--------------------------------------------------------------------------
*/

export async function getGovernmentSchemes({
  state,
  farmer_category,
  farm_size,
  crop,
  irrigation,
  gender,
  age,
}) {
  return request("/government/recommend", {
    method: "POST",

    body: JSON.stringify({
      state,
      farmer_category,
      farm_size,
      crop,
      irrigation,
      gender,
      age,
    }),
  });
}

/*
|--------------------------------------------------------------------------
| Knowledge Agent
|--------------------------------------------------------------------------
*/

export async function askKnowledgeAgent(question) {
  return request("/knowledge/ask", {
    method: "POST",

    body: JSON.stringify({
      question,
    }),
  });
}

/*
|--------------------------------------------------------------------------
| Orchestrator
|--------------------------------------------------------------------------
*/

export async function runOrchestrator(data) {
  return request("/orchestrator/run", {
    method: "POST",

    body: JSON.stringify(data),
  });
}