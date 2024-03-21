from furniture_analyze.process_plan import process_plan, Space

def test_process_plan():
    # Define a sample floor plan
    plan = """
    +-----------+------------------------------------+
    |           |            P SSSSS  P              |
    | (closet)  |            P        P              |
    |         P |            P P P P P               |
    |         P |             (conference room)      |
    +-----------+------------------------------------+
    |    (wc) C |                                    |
    +-----------+    W                         C     |
                |          (sleeping room)           |
                |                                    |
                |                                    |
                +--------------+---------------------+

    """

    # Call the process_plan function
    rooms = process_plan(plan)

    # Assert that the rooms list is not empty
    assert rooms

    # Assert that the first room is of type Space
    assert isinstance(rooms[0], Space)

    # Assert that the total furniture count is calculated correctly
    assert rooms[0].furn_count == {'W': 1, 'P': 11, 'C': 2, 'S': 5}, 'total number of charis estimated wrongly'

    # Assert that the total number of rooms is correct
    assert len(rooms)-1 == 4, 'number of rooms wrongly estimated'