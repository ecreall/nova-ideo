# GraphQL API

You can use [graphiql](https://github.com/graphql/graphiql) to explore the API.
graphiql is accessible at [http://localhost:6543/graphiql](http://localhost:6543/graphiql)

## Basic example:

    {
      ideas {
        edges {
          node { title }
        }
      }
    }

## Example:

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
