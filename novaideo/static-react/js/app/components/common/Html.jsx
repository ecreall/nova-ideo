// @flow
import React from 'react';
import activeHtml from 'react-active-html';

import { transformLinksInHtml } from '../../utils/linkify';
import Embed from './Embed';

type Props = {
  body: string,
  className: string
};

const bodyReplacementComponents = {
  iframe: (attributes) => {
    const { src } = attributes;
    return <Embed url={src} default={<iframe title="post-embed" {...attributes} />}/>
  }
};

const Html = (props: Props) => {
  const { body, className } = props;
  /*
   * The activeHtml() function will parse the raw html,
   * replace specified tags with provided components
   * and return a list of react elements
  */
  const nodes = activeHtml(transformLinksInHtml(body), bodyReplacementComponents);
  return (
    <div className={className}>
      {nodes}
    </div>
  );
};

export default Html;