# enspired-coding-task

## Furniture Analyze

Furniture Analyze is a Command Line Tool made in Python that allows you to analyze floor plans represented as text files to identify rooms and count furniture of different types within those rooms.
## Installation
### Prerequisites

Python 3.x installed on your system.


### Setup

After cloning the repository, navigate to the project directory:

```bash

cd enspired-coding-task

```

### Installation

Install the package and its dependencies using `pip`:

```bash

pip install .
```

This will install `furniture_analyze` package along with its dependencies.

### Usage
#### Analyzing Floor Plans

To analyse a floor plan in the form of a text file, use the provided command-line interface (CLI). For example, to analyze a file named rooms.txt, run:

```bash

furniture-analyze rooms.txt
```
This command will process the floor plan and print the analysis results to the console.

### Working
The algorithm reads in the plan in the form of a text file as a string. Wall components are identified by the characters `-|+/\`.  The process_plan function iterates over each row in the ascii string and identifies all non-wall components. These are saved as row-segments (for which a data class RowSegment is made). The RowSegment object contains the following information: row number, start and end coloumn of the non-wall region. 

As it iterates over row segments, it compares the current row segment with previous and checks if there is any overlap. If there is then it adds both row segments objects to a Space. A Space is another dataclass we created that stores several RowSegments that are not separated by walls. In this way we slowly build up a Space (which is a precursor to a room). 

Once there are no more overlapping row segments to be added (because it is blocked by wall components), we declare a Space object to be complete. We stop adding to that space. If there are more non-wall components encountered while iterating through the rows, we create a new Space object and add to this. 

Once we have finished iterating to all rows, we have some number of Space objects. We check whether it is a room depending on if it has text of the form `(<room name>)`. If it does the name attrirbute of the space object is assigned this name.

Finally, once all rooms are completely names, we identify furniture, count them and then count the total furniture in the floor plan.
