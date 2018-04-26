import React from 'react';

import { REGEXP } from '../../utils/globalFunctions';
import YoutubeEmbed from './YoutubeEmbed';
import SketchfabEmbed from './SketchfabEmbed';

const Embed = ({ url, ...props }) => {
  const isYoutubeVideo = url.match(REGEXP.youtube);
  if (isYoutubeVideo) return <YoutubeEmbed id={isYoutubeVideo[1]} {...props} />;
  const isSketchfab = url.match(REGEXP.sketchfab);
  if (isSketchfab) return <SketchfabEmbed id={isSketchfab[2]} {...props} />;
  return props.default;
};

export default Embed;