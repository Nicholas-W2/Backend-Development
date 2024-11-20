# Constellation Explorer API
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample constellation data
constellations = [
    {'id': 1, 'name': 'Orion', 'hemisphere': 'Northern', 'main_stars': ['Betelgeuse', 'Rigel', 'Bellatrix'], 'area': 594, 'origin': 'Greek'},
    {'id': 2, 'name': 'Scorpius', 'hemisphere': 'Southern', 'main_stars': ['Antares', 'Shaula', 'Sargas'], 'area': 497, 'origin': 'Greek'},
    {'id': 3, 'name': 'Ursa Major', 'hemisphere': 'Northern', 'main_stars': ['Dubhe', 'Merak', 'Phecda'], 'area': 1280, 'origin': 'Greek'},
    {'id': 4, 'name': 'Cassiopeia', 'hemisphere': 'Northern', 'main_stars': ['Schedar', 'Caph', 'Ruchbah'], 'area': 598, 'origin': 'Greek'},
    {'id': 5, 'name': 'Crux', 'hemisphere': 'Southern', 'main_stars': ['Acrux', 'Mimosa', 'Gacrux'], 'area': 68, 'origin': 'Latin'},
    {'id': 6, 'name': 'Lyra', 'hemisphere': 'Northern', 'main_stars': ['Vega', 'Sheliak', 'Sulafat'], 'area': 286, 'origin': 'Greek'},
    {'id': 7, 'name': 'Aquarius', 'hemisphere': 'Southern', 'main_stars': ['Sadalsuud', 'Sadalmelik', 'Sadachbia'], 'area': 980, 'origin': 'Babylonian'},
    {'id': 8, 'name': 'Andromeda', 'hemisphere': 'Northern', 'main_stars': ['Alpheratz', 'Mirach', 'Almach'], 'area': 722, 'origin': 'Greek'},
    {'id': 9, 'name': 'Pegasus', 'hemisphere': 'Northern', 'main_stars': ['Markab', 'Scheat', 'Algenib'], 'area': 1121, 'origin': 'Greek'},
    {'id': 10, 'name': 'Sagittarius', 'hemisphere': 'Southern', 'main_stars': ['Kaus Australis', 'Nunki', 'Ascella'], 'area': 867, 'origin': 'Greek'}
]

# The first endpoint is completed for your reference. Some endpoints have hints,
# and you must complete the others from scratch. Use principles of Uniform Interface.

# 1. View all constellations
# GET /constellations
@app.route('/constellations', methods=['GET'])
def get_all_constellations():
    return jsonify(constellations)

# 2. View a specific constellation by name
# GET /constellations/<name> (Path Parameter)
@app.route('/constellation/<name>', methods=['GET'])
def get_constellation_by_name(name):
    # Find the constellation by name (case-insensitive)
    constellation = next((constellation for constellation in constellations if constellation['name'].lower() == name.lower()), None)
    
    if constellation:
        return jsonify(constellation)
    else:
        return jsonify({'message': 'Constellation not found'}), 404

# 3. Add a new constellation
# POST /constellations, JSON body contains the constellation details

@app.route('/constellations', methods=['POST'])
def add_constellation():
    new_constellation = request.get_json()
    # Add validation if necessary (e.g., checking required fields)
    new_id = len(constellations) + 1  # Generating new id
    new_constellation['id'] = new_id
    constellations.append(new_constellation)
    return jsonify(new_constellation), 201  # Return 201 Created

# 4. Delete a constellation
@app.route('/constellations/<int:id>', methods=['DELETE'])
def delete_constellation(id):
    constellation = next((c for c in constellations if c['id'] == id), None)
    if constellation is None:
        return jsonify({"error": "Constellation not found"}), 404
    constellations.remove(constellation)
    return jsonify({"message": "Constellation deleted"}), 200


# 5. Filter constellations by hemisphere and area (Query String)
@app.route('/constellations', methods=['GET'])
def filter_constellations():
    hemisphere = request.args.get('hemisphere')
    min_area = request.args.get('min_area', type=int)

    filtered_constellations = constellations

    if hemisphere:
        filtered_constellations = [c for c in filtered_constellations if c['hemisphere'] == hemisphere]
    
    if min_area:
        filtered_constellations = [c for c in filtered_constellations if c['area'] >= min_area]

    return jsonify(filtered_constellations)


# 6. View the main stars of a constellation specified by name
@app.route('/constellations/<name>/main_stars', methods=['GET'])
def get_main_stars(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if constellation is None:
        return jsonify({"error": "Constellation not found"}), 404
    return jsonify(constellation['main_stars'])


# 7. Partially update a constellation specified by name
@app.route('/constellations/<name>', methods=['PATCH'])
def partial_update_constellation(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if constellation is None:
        return jsonify({"error": "Constellation not found"}), 404

    updates = request.get_json()
    for key, value in updates.items():
        if key in constellation:
            constellation[key] = value
    
    return jsonify(constellation)

# 8. For a constellation specified by name, view the image
# You might have to use an image generator API - try https://imagepig.com/
import requests

@app.route('/constellations/<name>/image', methods=['GET'])
def get_constellation_image(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if constellation is None:
        return jsonify({"error": "Constellation not found"}), 404

    # Use an image generation API like ImagePig (replace with actual API if needed)
    image_url = f"https://imagepig.com/generate?text={constellation['name']} constellation"
    
    return jsonify({"image_url": image_url})


# 9. Add your own! Try to use query strings or path parameters.
@app.route('/constellations/origin', methods=['GET'])
def get_constellations_by_origin():
    origin = request.args.get('origin')
    if not origin:
        return jsonify({"error": "Origin query parameter is required"}), 400
    
    filtered_constellations = [c for c in constellations if c['origin'].lower() == origin.lower()]
    
    return jsonify(filtered_constellations)


# 10. Double check that all the endpoints return the appropriate status codes.
# For errors, display the status code using an HTTP Cat - https://http.cat/


if __name__ == '__main__':
    app.run(debug=True)