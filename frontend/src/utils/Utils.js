const SHIPS = [{ship: "Carrier", "size": 5},
               {ship: "Battleship", "size": 4}, 
               {ship: "Submarine", "size": 3}, 
               {ship: "Cruiser" ,"size": 3}, 
               {ship: "Destroyer", "size": 2}]

export function get_ship(sub_phase) {
  const ship = sub_phase.split(" ")[0];
  if (get_ship_info(ship))
    return ship
  else 
    console.log("Undefined ship")
}

export function get_ship_info(ship_name) {
  const found = SHIPS.find(element => element['ship'] === ship_name);
  return found
}

export function next_ship(sub_phase) {
  let ship_name = get_ship(sub_phase);
  let index = SHIPS.findIndex(function (element) {
    return ship_name == element['ship'];
  });
  let next_val = index + 1;
  return next_val < SHIPS.length ? SHIPS[next_val]["ship"] + " Start" : "Submit Ships";
}

export function fill_gaps(start, end) {
  let diff_a = Math.abs(start[0] - end[0]);
  let diff_b = Math.abs(start[1] - end[1]);
  let locs = [];
  let diff, axis;
  if (diff_a > 0) {
    diff = diff_a;
    axis = 0;
  } else {
    diff = diff_b;
    axis = 1;
  }
  for (let i = 0; i <= diff; i++) {
    let loc = [];
    loc.push(axis == 0 ? Math.min(start[0], end[0]) + i : start[0]);
    loc.push(axis == 1 ? Math.min(start[1], end[1]) + i : start[1]);
    locs.push(loc);
  }
  return locs;
}

export function locations_equal(loc_a, loc_b) {
  return loc_a[0] == loc_b[0] && loc_a[1] == loc_b[1];
}

export function check_collisions(position_list, loc) {
  return position_list.findIndex(function (elem) {
    return locations_equal(elem, loc);
  });
}
