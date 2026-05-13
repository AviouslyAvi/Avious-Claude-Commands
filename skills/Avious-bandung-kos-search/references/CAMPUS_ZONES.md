# Bandung campus zones

Anchor coordinates and surrounding kos clusters for the most common "near campus X" queries. Use these to construct Mamikos geo searches (`/cari/{lat},{lng}/...?radius=N`).

## ITB (Institut Teknologi Bandung)

- **Anchor**: `-6.8915, 107.6107` (main campus, Jl. Ganesha)
- **Kos clusters** (kelurahan / common street names):
  - **Cisitu** — quietest, north of campus
  - **Sangkuriang** — west of campus, walkable
  - **Tubagus Ismail** — east, denser kos density
  - **Plesiran** — south, closest to campus gate
  - **Dipatiukur** — south, mixed Unpad / ITB student crowd
  - **Dago Pojok** — further north, hilly, cooler
- Default radius for "near ITB": **2 km**

## Unpad (Universitas Padjadjaran)

Unpad has TWO main locations — disambiguate before searching:

### Unpad Dipatiukur (in-city, undergrad some + grad)
- **Anchor**: `-6.8898, 107.6147`
- Kos cluster overlaps with the ITB cluster — use the same anchor + 2km radius.

### Unpad Jatinangor (main undergrad campus)
- **Anchor**: `-6.9275, 107.7733`
- ⚠️ This is **Sumedang regency**, not Bandung city — about 25km east. Mamikos searches scoped to "Bandung" may miss it. Search by coordinates instead, with radius 1.5 km. Confirm with the user before including Jatinangor results in a "Bandung" search.

## Maranatha (Universitas Kristen Maranatha)

- **Anchor**: `-6.8939, 107.5870`
- **Kos clusters**: Suria Sumantri, Surya Sumantri, Pasirkaliki, Babakan Jeruk
- Default radius: **1.5 km**

## Telkom University (Tel-U)

- **Anchor**: `-6.9733, 107.6303` (Bandung Technoplex / Sukabirus)
- **Kos clusters**: Sukabirus, Sukapura, Buah Batu south, Dayeuhkolot
- ⚠️ South Bandung — separate kos market from ITB/Unpad. Different prices.
- Default radius: **2 km**

## Unisba / Unpas (city-center universities)

- **Anchor**: `-6.9072, 107.6098` (Tamansari area)
- **Kos clusters**: Tamansari, Cihampelas, Setiabudhi (lower)
- Default radius: **1.5 km**

## City-wide fallback

If no campus is specified and the user just says "Bandung":
- Use the city slug `bandung-kota-bandung-jawa-barat-indonesia` instead of coordinates.
- No radius needed — Mamikos returns city-scoped results.

## Neighborhood lifestyle hints (for soft scoring or user reminders)

- **Cooler / hillier**: Dago, Ciumbuleuit, Setiabudi, Lembang (last is outside city)
- **Walkable / heritage**: Riau, Braga, Asia-Afrika
- **Mall-adjacent / modern**: Pasteur, Sukajadi, Setrasari
- **Budget-friendlier**: Buahbatu, Margahayu, Soekarno-Hatta corridor
- **Avoid for residential quiet**: industrial belts, Cibaduyut traffic spine
