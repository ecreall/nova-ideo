// @flow
import React from 'react';
import activeHtml from 'react-active-html';

import { transformLinksInHtml } from '../../utils/linkify';
import { youtubeRegexp } from '../../utils/globalFunctions';
import YoutubeTheater from './YoutubeTheater';

type Props = {
  body: string,
  className: string
};

const bodyReplacementComponents = {
  iframe: (attributes) => {
    const { src } = attributes;
    const regexpMatch = src.match(youtubeRegexp);
    if (regexpMatch) {
      const videoId = regexpMatch[1];
      return <YoutubeTheater videoId={videoId} />;
    }
    return <iframe title="post-embed" {...attributes} />;
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