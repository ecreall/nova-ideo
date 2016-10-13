import React from 'react';
import ReactDOM from 'react-dom';

import { GraphQLDocs } from 'graphql-docs';

function fetcher(query) {
    return fetch(window.location.origin + '/graphql', {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
        }),
    }).then(function(r) {
        return r.json();
    });
}

const rootElement = document.getElementById('root')

ReactDOM.render(
  <GraphQLDocs fetcher={fetcher} />,
  rootElement
);
