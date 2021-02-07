from flask import request, abort, Response, stream_with_context
import urllib.parse


class Auto():
    endpoints = ['/auto/<channel>', '/hdhr/auto/<channel>']
    endpoint_name = "hdhr_auto"

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.bytes_per_read = int(self.fhdhr.config.dict["streaming"]["bytes_per_read"])

    @property
    def source(self):
        return self.fhdhr.config.dict["hdhr"]["source"] or self.fhdhr.origins.valid_origins[0]

    def __call__(self, channel, *args):
        return self.get(channel, *args)

    def get(self, channel, *args):

        origin = self.source

        redirect_url = "/api/tuners?method=stream"

        if channel.startswith("v"):
            channel_number = channel.replace('v', '')
        elif channel.startswith("ch"):
            channel_freq = channel.replace('ch', '').split("-")[0]
            subchannel = None
            if "-" in channel:
                subchannel = channel.replace('ch', '').split("-")[1]
            if subchannel:
                self.fhdhr.logger.error("Not Implemented %s-%s" % (channel_freq, subchannel))
                abort(501, "Not Implemented %s-%s" % (channel_freq, subchannel))
            else:
                self.fhdhr.logger.error("Not Implemented %s" % (channel_freq, subchannel))
                abort(501, "Not Implemented %s" % channel_freq)
        else:
            channel_number = channel

        redirect_url += "&channel=%s" % str(channel_number)
        redirect_url += "&origin=%s" % str(origin)
        redirect_url += "&stream_method=%s" % self.fhdhr.origins.origins_dict[origin].stream_method

        duration = request.args.get('duration', default=0, type=int)
        if duration:
            redirect_url += "&duration=%s" % str(duration)

        transcode_quality = request.args.get('transcode', default=None, type=str)
        if transcode_quality:
            redirect_url += "&transcode=%s" % str(transcode_quality)

        redirect_url += "&accessed=%s" % urllib.parse.quote(request.url)

        def generate():

            try:

                chunk_counter = 1

                while True:

                    for chunk in self.fhdhr.api.get(redirect_url, chunk_size=self.bytes_per_read):

                        if not chunk:
                            break
                        yield chunk

                        chunk_counter += 1

            except GeneratorExit:
                self.fhdhr.logger.info("Internal API Connection Closed.")
            except Exception as e:
                self.fhdhr.logger.info("Internal API Connection Closed: %s" % e)
            finally:
                self.fhdhr.logger.info("Internal API Connection Closed.")

        return Response(stream_with_context(generate()))
