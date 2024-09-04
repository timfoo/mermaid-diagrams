mermaid_examples = {
    "diagrams": [
        {
            "id": 1,
            "title": "Sequence Diagram",
            "description": "A Sequence diagram is an interaction diagram that shows how processes operate with one another and in what order.",
            "diagram_examples": [
                {
                    """
                    ---
                    title: Simple example
                    ---
                    sequenceDiagram
                        Alice->>John: Hello John, how are you?
                        John-->>Alice: Great!
                        Alice-)John: See you later!
                    """

                },
                {
                    """
                    ---
                    title: Simple example with note
                    ---
                    sequenceDiagram
                        Alice ->> Bob: Hello Bob, how are you?
                        Bob-->>John: How about you John?
                        Bob--x Alice: I am good thanks!
                        Bob-x John: I am good thanks!
                        Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

                        Bob-->Alice: Checking with John...
                        Alice->John: Yes... John, how are you?
                    """

                },
                {
                    """
                    ---
                    title: Loops, Alt and Opt
                    ---
                    sequenceDiagram
                        loop Daily query
                            Alice->>Bob: Hello Bob, how are you?
                            alt is sick
                                Bob->>Alice: Not so good :(
                            else is well
                                Bob->>Alice: Feeling fresh like a daisy
                            end

                            opt Extra response
                                Bob->>Alice: Thanks for asking
                            end
                        end
                    """
                },
                {
                    """
                    ---
                    title: Message to self in loop
                    ---
                    sequenceDiagram
                        loop Daily query
                            Alice->>Bob: Hello Bob, how are you?
                            alt is sick
                                Bob->>Alice: Not so good :(
                            else is well
                                Bob->>Alice: Feeling fresh like a daisy
                            end

                            opt Extra response
                                Bob->>Alice: Thanks for asking
                            end
                        end
                    """
                },
                {
                    """
                    ---
                    title: Blogging app service communication
                    ---
                    sequenceDiagram
                        participant web as Web Browser
                        participant blog as Blog Service
                        participant account as Account Service
                        participant mail as Mail Service
                        participant db as Storage

                        Note over web,db: The user must be logged in to submit blog posts
                        web->>+account: Logs in using credentials
                        account->>db: Query stored accounts
                        db->>account: Respond with query result

                        alt Credentials not found
                            account->>web: Invalid credentials
                        else Credentials found
                            account->>-web: Successfully logged in

                            Note over web,db: When the user is authenticated, they can now submit new posts
                            web->>+blog: Submit new post
                            blog->>db: Store post data

                            par Notifications
                                blog--)mail: Send mail to blog subscribers
                                blog--)db: Store in-site notifications
                            and Response
                                blog-->>-web: Successfully posted
                            end
                        end
                    """
                }
            ]
        },
        # {
        #     "id": 2,
        #     "title": "User Journey Diagram",
        #     "description": "User journeys describe at a high level of detail exactly what steps different users take to complete a specific task within a system, application or website. This technique shows the current (as-is) user workflow, and reveals areas of improvement for the to-be workflow.",
        #     "diagram": """
        #         journey
        #             title My working day
        #             section Go to work
        #                 Make tea: 5: Me
        #                 Go upstairs: 3: Me
        #                 Do work: 1: Me, Cat
        #             section Go home
        #                 Go downstairs: 5: Me
        #                 Sit down: 5: Me
        #     """
        # },
        {
            "id": 3,
            "title": "Mindmap",
            "description": "A mind map is a diagram used to visually organize information into a hierarchy, showing relationships among pieces of the whole. It is often created around a single concept, drawn as an image in the center of a blank page, to which associated representations of ideas such as images, words and parts of words are added. Major ideas are connected directly to the central concept, and other ideas branch out from those major ideas.",
            "diagram_examples": [
                {
                    """
                    mindmap
                        root(Cofinder)  
                            (Introduction)  
                            ::icon(fa fa-info-circle)  
                            (Designed to help the Cohere Community find relevant content)  
                            (Users can ask natural language questions)  
                            (Semantic search tool that brings together information from multiple sources)  
                            (Repository Contents)  
                            ::icon(fa fa-folder-open)  
                            (cohere_text_preprocessing.csv)  
                            (preprocessing.ipynb)  
                            (main.py)  
                            (cohere_text_final.csv)  
                            (search_index.ann)  
                            (Five Steps to Building the Application)  
                            ::icon(fa fa-list-ol)  
                            (Data Sources)  
                                (Pre-processing the article text into chunks)  
                            (Embeddings & Search Index)  
                                (Use co.embed to obtain a vector representation of data)  
                                (Store embeddings in a vector database)  
                            (Front End)  
                                (Streamlit for user interaction)  
                            (Search)  
                                (Use co.embed to get vector representation of user query)  
                                (Use nearest neighbours to return relevant content)  
                            (Answer)  
                                (Use co.generate to answer the query given the context from the search results and the question)  
                            (Streamlit Application)  
                            ::icon(fa fa-desktop)  
                            (Load libraries, data and search index)  
                            (Add functions to generate embeddings to search the Annoy index for the users query)  
                            (Generate an answer from the context)  
                            (Add Streamlit search input and button to run functions)
                    """
                },
                {
                    """
                        mindmap
                            root((mindmap))
                                Origins
                                    Long history
                                    Popularisation
                                        British popular psychology author Tony Buzan
                                Research
                                    On effectiveness<br/>and features
                                    On Automatic creation
                                        Uses
                                            Creative techniques
                                            Strategic planning
                                            Argument mapping
                                Tools
                                    Pen and paper
                                    Mermaid
                            id1["`**Root** with
                                a second line
                                Unicode works too: 🤓`"]
                                id2["`The dog in **the** hog... a *very long text* that wraps to a new line`"]
                                id3[Regular labels still works]
                        """
                }
            ]
        },
        {
            "id": 4,
            "title": "Flowcharts",
            "description": "Flowcharts are composed of nodes (geometric shapes) and edges (arrows or lines). The Mermaid code defines how nodes and edges are made and accommodates different arrow types, multi-directional arrows, and any linking to and from subgraphs.",
            "diagram_examples": [
                {
                    """
                    ---
                    title: Formatting and Subgraphs
                    ---
                    flowchart LR
                        id
                        id1[This is the text in the box]
                        id2 
                        markdown["`This **is** _Markdown_`"]
                        
                        id --> id1
                        id1 -- This is text on the link -->id2
                        id1 --> id2 & markdown
                        id2 & markdown --> id

                        subgraph subgraph1
                            direction TB
                            top1[top] --> bottom1[bottom]
                        end

                        subgraph subgraph2
                            direction TB
                            top2[top] --> bottom2[bottom]
                        end

                        id --> subgraph 1
                        id --> subgraph 2
                    """
                },
                {
                    """
                    ---
                    title: What to do if it is raining
                    ---
                    flowchart LR
                        id
                        id1[This is the text in the box]
                        id2 
                        markdown["`This **is** _Markdown_`"]
                        
                        id --> id1
                        id1 -- This is text on the link -->id2
                        id1 --> id2 & markdown
                        id2 & markdown --> id

                        subgraph subgraph1
                            direction TB
                            top1[top] --> bottom1[bottom]
                        end

                        subgraph subgraph2
                            direction TB
                            top2[top] --> bottom2[bottom]
                        end

                        id --> subgraph 1
                        id --> subgraph 2
                    """
                },
                {
                    """
                    ---
                    title: Larger flowchart with some styling
                    ---
                    flowchart TB
                        sq[Square shape] --> ci((Circle shape))

                        subgraph A
                            od>Odd shape]-- Two line<br/>edge comment --> ro
                            di{Diamond with <br/> line break} -.-> ro(Rounded<br>square<br>shape)
                            di==>ro2(Rounded square shape)
                        end

                        %% Notice that no text in shape are added here instead that is appended further down
                        e --> od3>Really long text with linebreak<br>in an Odd shape]

                        %% Comments after double percent signs
                        e((Inner / circle<br>and some odd <br>special characters)) --> f(,.?!+-*ز)

                        cyr[Cyrillic]-->cyr2((Circle shape Начало));

                        classDef green fill:#9f6,stroke:#333,stroke-width:2px;
                        classDef orange fill:#f96,stroke:#333,stroke-width:4px;
                        class sq,e green
                        class di orange

                    """
                },
            ]
        }
    ]
}