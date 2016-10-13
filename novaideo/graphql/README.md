Example:

    query MyQuery ($after: String) {
      results: ideas(
          first: 30,
          after: $after) {
        pageInfo{
          endCursor,
          hasNextPage,
        },
        edges{
          node{
            title,
            keywords,
          }
        }
      }
    }

Query variables :

    {"after": ""}

