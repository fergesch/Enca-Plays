const SHIPS = ["Carrier", "Battleship", "Submarine", "Cruiser", "Destroyer"];

export function next_ship(sub_phase) {
  let ship_name = sub_phase.split(" ")[0];
  let index = SHIPS.findIndex(function (element) {
    return ship_name == element;
  });
  let next_val = index + 1;
  return next_val < SHIPS.length ? SHIPS[next_val] + " Start" : "Submit Ships";
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
