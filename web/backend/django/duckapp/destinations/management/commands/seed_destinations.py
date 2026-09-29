"""
Seed a repeatable starter catalog of openly licensed Zimbabwe destination photos.
"""

from django.core.management.base import BaseCommand

from web.backend.django.duckapp.destinations.models import Destination


DESTINATIONS = [
    {
        "name": "Victoria Falls",
        "location": "Victoria Falls, Matabeleland North",
        "category": "Nature",
        "description": "A vast waterfall on the Zambezi River and one of the world's most celebrated natural landmarks.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/13/Cataratas_Victoria%2C_Zambia-Zimbabue%2C_2018-07-27%2C_DD_16-20_PAN.jpg/960px-Cataratas_Victoria%2C_Zambia-Zimbabue%2C_2018-07-27%2C_DD_16-20_PAN.jpg",
        "image_credit": "Diego Delso — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Cataratas_Victoria,_Zambia-Zimbabue,_2018-07-27,_DD_16-20_PAN.jpg",
    },
    {
        "name": "Great Zimbabwe",
        "location": "Masvingo, Masvingo",
        "category": "Historical",
        "description": "The monumental stone remains of the medieval city that gave Zimbabwe its name and served as a regional centre of trade.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7c/Great-Zimbabwe-ruins-outer-walls-3-1200.jpg/960px-Great-Zimbabwe-ruins-outer-walls-3-1200.jpg",
        "image_credit": "Edwin Smith and Andrew Dale — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Great-Zimbabwe-ruins-outer-walls-3-1200.jpg",
    },
    {
        "name": "Hwange National Park",
        "location": "Hwange, Matabeleland North",
        "category": "Wildlife",
        "description": "Zimbabwe's largest national park, known for its elephants, varied habitats, and wildlife viewing.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f2/Hwange_National_Park%2C_Zimbabwe_%2848594790636%29.jpg/960px-Hwange_National_Park%2C_Zimbabwe_%2848594790636%29.jpg",
        "image_credit": "Fabio Achilli — CC BY 2.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Hwange_National_Park,_Zimbabwe_(48594790636).jpg",
    },
    {
        "name": "Mana Pools National Park",
        "location": "Hurungwe, Mashonaland West",
        "category": "Wildlife",
        "description": "A UNESCO-listed Zambezi floodplain wilderness known for river scenery, wildlife, and walking safaris.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bd/Island_in_the_Zambezi_River_at_Mana_Pools_National_Park-1.jpg/960px-Island_in_the_Zambezi_River_at_Mana_Pools_National_Park-1.jpg",
        "image_credit": "Babakathy — CC0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Island_in_the_Zambezi_River_at_Mana_Pools_National_Park-1.jpg",
    },
    {
        "name": "Matobo Hills",
        "location": "Matobo, Matabeleland South",
        "category": "Nature",
        "description": "Granite kopjes, ancient rock art, and dramatic landscapes in a UNESCO-listed cultural landscape.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Sunrise_Matobo_Zimbabwe.jpg",
        "image_credit": "Macvivo (original: Samwise Gamgee) — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Sunrise_Matobo_Zimbabwe.jpg",
    },
    {
        "name": "Lake Kariba",
        "location": "Kariba, Mashonaland West",
        "category": "Lake",
        "description": "A vast reservoir on the Zambezi, with lakeside towns, islands, and houseboat excursions.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/47/Kariba%2C_Zimbabwe_01.JPG/960px-Kariba%2C_Zimbabwe_01.JPG",
        "image_credit": "Suesen — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Kariba,_Zimbabwe_01.JPG",
    },
    {
        "name": "Chimanimani National Park",
        "location": "Chimanimani, Manicaland",
        "category": "Mountains",
        "description": "A highland park of rugged peaks, forests, waterfalls, and hiking trails near the Mozambique border.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/Chimanimani_banner.png/960px-Chimanimani_banner.png",
        "image_credit": "Manfidza — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Chimanimani_banner.png",
    },
    {
        "name": "Nyanga National Park",
        "location": "Nyanga, Manicaland",
        "category": "Mountains",
        "description": "Eastern Highlands scenery with mountain slopes, rivers, waterfalls, and archaeological sites.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/96/Central_nyanga_np.jpg",
        "image_credit": "Babakathy — Public domain",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Central_nyanga_np.jpg",
    },
    {
        "name": "Gonarezhou National Park",
        "location": "Chiredzi, Masvingo",
        "category": "Wildlife",
        "description": "A large southern wilderness reserve whose name means 'Place of Elephants' in the local Shona language.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6a/Zimbabwe_Gonarezhou_Landscape_Chilojo_Cliffs.jpg/960px-Zimbabwe_Gonarezhou_Landscape_Chilojo_Cliffs.jpg",
        "image_credit": "Ralf Ellerich — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Zimbabwe_Gonarezhou_Landscape_Chilojo_Cliffs.jpg",
    },
    {
        "name": "Chinhoyi Caves",
        "location": "Chinhoyi, Mashonaland West",
        "category": "Nature",
        "description": "A limestone cave system featuring the striking, clear blue waters of the Sleeping Pool.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b0/Chinhoyi_caves%2C_Zimbabwe.JPG/960px-Chinhoyi_caves%2C_Zimbabwe.JPG",
        "image_credit": "Suesen — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Chinhoyi_caves,_Zimbabwe.JPG",
    },
    {
        "name": "Zambezi National Park",
        "location": "Victoria Falls, Matabeleland North",
        "category": "Wildlife",
        "description": "A riverside national park west of Victoria Falls, with wildlife habitats along the upper Zambezi.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/be/Facocero_com%C3%BAn_%28Phacochoerus_africanus%29%2C_parque_nacional_de_Zambeze%2C_Zimbabue%2C_2018-07-28%2C_DD_01.jpg/960px-Facocero_com%C3%BAn_%28Phacochoerus_africanus%29%2C_parque_nacional_de_Zambeze%2C_Zimbabue%2C_2018-07-28%2C_DD_01.jpg",
        "image_credit": "Diego Delso — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Facocero_com%C3%BAn_(Phacochoerus_africanus),_parque_nacional_de_Zambeze,_Zimbabue,_2018-07-28,_DD_01.jpg",
    },
    {
        "name": "Bvumba Mountains",
        "location": "Mutare, Manicaland",
        "category": "Mountains",
        "description": "A green mountain range near Mutare, known for misty viewpoints, forests, and birdwatching.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1a/Bvumba_mountains.JPG/960px-Bvumba_mountains.JPG",
        "image_credit": "Graph Geo — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Bvumba_mountains.JPG",
    },
    {
        "name": "Mount Nyangani",
        "location": "Nyanga, Manicaland",
        "category": "Mountains",
        "description": "Zimbabwe's highest mountain, rising above the Eastern Highlands within Nyanga National Park.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Nyangani_from_nyamuziwa_source.jpg",
        "image_credit": "Babakathy — Public domain",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Nyangani_from_nyamuziwa_source.jpg",
    },
    {
        "name": "Domboshava Caves",
        "location": "Domboshava, Mashonaland East",
        "category": "Historical",
        "description": "A granite hill site near Harare with rock shelters and ancient San rock paintings.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a1/Domboshawa_%282%29.jpg/960px-Domboshawa_%282%29.jpg",
        "image_credit": "Fanny Schertzer — CC BY 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Domboshawa_(2).jpg",
    },
    {
        "name": "Naletale Ruins",
        "location": "Shurugwi, Midlands",
        "category": "Historical",
        "description": "Stone ruins in the Shurugwi area, known for their patterned walls and links to the Rozvi state.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0a/Gweru_banner_Naletale_Ruins.png/960px-Gweru_banner_Naletale_Ruins.png",
        "image_credit": "Fanny Schertzer — CC BY 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Gweru_banner_Naletale_Ruins.png",
    },
    {
        "name": "Khami Ruins",
        "location": "Bulawayo, Bulawayo",
        "category": "Historical",
        "description": "The remains of a former Kingdom of Butua capital, now a UNESCO World Heritage Site.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/47/Khami_ruins_%28Zimbabwe%29_banner.jpg/960px-Khami_ruins_%28Zimbabwe%29_banner.jpg",
        "image_credit": "Digr — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Khami_ruins_(Zimbabwe)_banner.jpg",
    },
    {
        "name": "Mutarazi Falls",
        "location": "Nyanga, Manicaland",
        "category": "Nature",
        "description": "Zimbabwe's tallest waterfall, plunging from the Eastern Highlands escarpment.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a8/Mtarazi_falls.jpg/960px-Mtarazi_falls.jpg",
        "image_credit": "Seabifar — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Mtarazi_falls.jpg",
    },
    {
        "name": "Lake Chivero Recreational Park",
        "location": "Lake Chivero, Mashonaland West",
        "category": "Lake",
        "description": "A lakeside recreation and wildlife area west of Harare, popular for birdwatching and day trips.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/16/COSV_-_Zimbabwe_2011_-_Lake_Chivero.jpg/960px-COSV_-_Zimbabwe_2011_-_Lake_Chivero.jpg",
        "image_credit": "COSV — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:COSV_-_Zimbabwe_2011_-_Lake_Chivero.jpg",
    },
    {
        "name": "Chiremba Balancing Rocks",
        "location": "Epworth, Harare Metropolitan",
        "category": "Nature",
        "description": "A cluster of distinctive balancing rock formations at the Chiremba site near Epworth.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2d/Chiremba_Balancing_Rocks_-_Harare3500.jpg/960px-Chiremba_Balancing_Rocks_-_Harare3500.jpg",
        "image_credit": "lumoplank — CC0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Chiremba_Balancing_Rocks_-_Harare3500.jpg",
    },
    {
        "name": "Chirinda Forest",
        "location": "Chipinge, Manicaland",
        "category": "Nature",
        "description": "A remnant tropical forest reserve in the Chipinge district, home to unusual plant and animal life.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/60/Dracaena_fragrans%2C_Chirinda_Forest%2C_Bart_Wursten.jpg",
        "image_credit": "Bart Wursten — CC BY-SA 3.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Dracaena_fragrans,_Chirinda_Forest,_Bart_Wursten.jpg",
    },
    {
        "name": "Antelope Park",
        "location": "Gweru, Midlands",
        "category": "Wildlife",
        "description": "A wildlife conservation and visitor centre near Gweru with opportunities to learn about African wildlife.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Lioness_at_Antelope_Park_%21_%2815033223934%29.jpg/960px-Lioness_at_Antelope_Park_%21_%2815033223934%29.jpg",
        "image_credit": "Mara 1 — CC BY 2.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Lioness_at_Antelope_Park_!_(15033223934).jpg",
    },
    {
        "name": "Chipangali Wildlife Orphanage",
        "location": "Bulawayo, Bulawayo",
        "category": "Wildlife",
        "description": "A wildlife rescue and rehabilitation centre outside Bulawayo focused on rescued indigenous animals.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/75/Roxy_the_Leopard.jpg",
        "image_credit": "Clivetagwi — CC BY-SA 4.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Roxy_the_Leopard.jpg",
    },
    {
        "name": "Ewanrig Botanical Garden",
        "location": "Harare, Harare Metropolitan",
        "category": "Nature",
        "description": "A Harare botanical garden and birding site showcasing native and cultivated plant collections.",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/df/Red-throated_twinspot%2C_Hypargos_niveoguttatus_at_Ewanrig_Botanical_Garden%2C_Harare%2C_Zimbabwe_%2821817901876%29.jpg/960px-Red-throated_twinspot%2C_Hypargos_niveoguttatus_at_Ewanrig_Botanical_Garden%2C_Harare%2C_Zimbabwe_%2821817901876%29.jpg",
        "image_credit": "Derek Keats — CC BY 2.0",
        "image_source_url": "https://commons.wikimedia.org/wiki/File:Red-throated_twinspot,_Hypargos_niveoguttatus_at_Ewanrig_Botanical_Garden,_Harare,_Zimbabwe_(21817901876).jpg",
    },
]


class Command(BaseCommand):
    """
    Inserts or refreshes the starter destination records without duplicating them.
    """

    help = "Seed the database with Zimbabwe destinations and licensed photo links."

    def handle(self, *args, **options):
        for destination in DESTINATIONS:
            name = destination["name"]
            location = destination["location"]
            defaults = {
                key: value
                for key, value in destination.items()
                if key not in {"name", "location"}
            }
            Destination.objects.update_or_create(
                name=name,
                location=location,
                defaults=defaults,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(DESTINATIONS)} Zimbabwe destinations."
            )
        )
