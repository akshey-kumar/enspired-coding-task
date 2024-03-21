from typing import List, Dict
import re
from dataclasses import dataclass, field

@dataclass
class RowSegment:
    """
    Represents segment of a row including non-wall elements.

    Attributes:
        row_no (int): The row number.
        col_start (int): The starting column index.
        col_end (int): The ending column index.
        text (str): The text content of the segment.

    Methods:
        check_overlap(self, row_segment_2): Check if two row segments overlap along the horizontal axis.
    """
    row_no: int
    col_start: int
    col_end: int
    text: str

    def check_overlap(self, row_segment_2):
        """Check if two row segments overlap along the horizontal axis."""
        return max(self.col_start, row_segment_2.col_start) < min(self.col_end, row_segment_2.col_end)


    def __repr__(self):
        return f'{self.row_no}:{self.col_start}-{self.col_end}'


@dataclass
class Space:
    """
    Represents a space in a floor plan. A space with a name is a room.

    Attributes:
        name (str): The name of the space.
        furn_count (Dict[str, int]): The count of furniture types in the space.
        segments (List[RowSegment]): The list of row segments in the space.
        is_complete (bool): Indicates if the space is complete.
        is_room (bool): Indicates if the space is a room.

    Methods:
        analyze_space(self): Extract name and count furniture in the space.
    """
    name: str = 'noname'
    furn_count: Dict[str, int] = field(default_factory=dict)
    segments: List[RowSegment] = field(default_factory=list)
    is_complete: bool = False
    is_room: bool = False

    def analyze_space(self):
        """Extract name and count furniture in the space."""
        text = ''.join(s.text for s in self.segments)
        name_match = re.search(r'\(.*?\)', text)

        if name_match:
            self.is_room = True
            self.name = name_match.group(0)[1:-1]
            self.furn_count = {furniture_type: text.count(furniture_type) for furniture_type in 'WPSC'}

        return self.name, self.furn_count

    def __repr__(self):
        furniture_counts = ', '.join([f'{furniture}: {count}' for furniture, count in self.furn_count.items()])
        return f'{self.name}:\n{furniture_counts}'


def sort_rooms(rooms: List[Space]) -> List[Space]:
    """
    Sort a list of rooms alphabetically by their name and calculate total furniture.
    """
    sorted_rooms = sorted(rooms, key=lambda space: space.name)
    total = {k: sum(room.furn_count[k] for room in sorted_rooms) for k in sorted_rooms[0].furn_count.keys()}
    tot = Space(name='total', furn_count = total)
    sorted_rooms[:0] = [tot]
    return sorted_rooms


def process_plan(plan):
    """
    Parse the floor plan, identify spaces, and analyze them by counting furniture.

    Parameters:
        plan (str): The floor plan represented as a string.

    Returns:
        List[Space]: A list of identified rooms in the floor plan.
    """
    # Initialize lists to hold spaces and rooms
    spaces = []
    rooms = []

    # Split the floor plan into rows and skip the first row (header)
    rows = plan.split('\n')[1:]

    # Iterate over each row in the floor plan
    for row_no, row in enumerate(rows):
        # Find non-wall segments  within the row
        found_segments = [RowSegment(row_no, segment.start(), segment.end(), segment.group()) for segment in re.finditer(r'[^/\\|+-]+', row)]

        for space in spaces:
            segments_added = False

            # Iterate over segments and add them to the space if they overlap with the last row in the space
            for segment in found_segments:
                if segment.check_overlap(space.segments[-1]):
                    space.segments.append(segment)
                    found_segments.remove(segment)
                    segments_added = True
                    break

            # If no segments were added to the space, mark it as complete
            if not segments_added:
                space.is_complete = True
                space.analyze_space()
                if space.is_room:
                    rooms.append(space)

        # Remove complete spaces from the list
        spaces = [space for space in spaces if not space.is_complete]

        # Create new spaces for remaining segments
        for segment in found_segments:
            new_space = Space()
            new_space.segments.append(segment)
            spaces.append(new_space)

    # Sort the list of rooms alphabetically by their name
    sorted_rooms = sort_rooms(rooms)

    # Calculate the total furniture count across all rooms
    total = {k: sum(room.furn_count[k] for room in rooms) for k in rooms[0].furn_count.keys()}
    Space(name='total',
          furn_count = total)
    return sorted_rooms
