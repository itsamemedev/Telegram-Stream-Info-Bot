# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (172)

```
 10448  GET              /                                                dashboard
 14319  GET              /api/abo/status                                  api_abo_status
 10521  GET              /api/active-recordings                           api_active_recordings
 14390  GET              /api/activity-pulse                              api_activity_pulse
 14197  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21075  GET/POST         /api/audio/config                                api_audio_config
 21105  POST             /api/audio/testtone                              api_audio_testtone
 14263  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14287  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14291  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11975  GET              /api/automation/status                           api_automation_status
 11997  POST             /api/automation/toggle                           api_automation_toggle
 13194  GET              /api/azrael/agents                               api_azrael_agents
 11867  POST             /api/azrael/ask                                  api_azrael_ask
 21311  GET/POST         /api/azrael/context                              api_azrael_context
 12899  GET              /api/azrael/core                                 api_azrael_core
 21445  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21435  GET              /api/azrael/live_status                          api_azrael_live_status
 21453  POST             /api/azrael/live_test                            api_azrael_live_test
 13203  GET              /api/azrael/memories                             api_azrael_memories
 21501  POST             /api/azrael/persona                              api_azrael_persona_set
 21492  GET              /api/azrael/personas                             api_azrael_personas
 21529  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21284  POST             /api/azrael/react                                api_azrael_react
 21320  GET              /api/azrael/reaction                             api_azrael_reaction
 21472  GET              /api/azrael/reactions                            api_azrael_reactions
 21522  GET              /api/azrael/transcript                           api_azrael_transcript
 21407  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21382  GET              /api/azrael/voices                               api_azrael_voices
 21546  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10820  GET              /api/backoff-watch                               api_backoff_watch
 13678  POST             /api/backup/run                                  api_backup_run
 13644  GET              /api/backup/status                               api_backup_status
 13633  POST             /api/backup/system                               api_backup_system
 14229  GET              /api/bandwidth/live                              api_bandwidth_live
 14182  GET              /api/bookmarks                                   api_bookmarks_list
 11083  GET              /api/brain                                       api_brain
 11020  GET              /api/brain/alarms                                api_brain_alarms
 11005  GET              /api/brain/creator                               api_brain_creator
 10982  GET              /api/brain/graph                                 api_brain_graph
 11043  GET              /api/brain/growth                                api_brain_growth
  9998  GET              /api/brain/health                                api_brain_health
 22027  GET              /api/channel/categories                          api_channel_categories
 22033  POST             /api/channel/set                                 api_channel_set
 21843  GET              /api/channels/status                             api_channels_status
 20719  POST             /api/chat/send                                   api_chat_send
 13398  GET              /api/chat/send_status                            api_chat_send_status
 10502  GET              /api/checks                                      api_checks
 21348  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21331  GET              /api/clips                                       api_clips
 21364  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20997  GET              /api/cohost                                      api_cohost
 21009  POST             /api/cohost/config                               api_cohost_config
 14698  GET              /api/community/stats                             api_community_stats
 22667  GET              /api/data/export                                 api_data_export
 20923  GET              /api/debug/threads                               api_debug_threads
 23494  GET              /api/defense/attacks                             api_defense_attacks
 23461  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23479  GET              /api/defense/fail2ban                            api_defense_fail2ban
 23185  GET              /api/defense/overview                            api_defense_overview
 13740  POST             /api/discord/announce                            api_discord_announce
 13468  GET              /api/discord/clips_week                          api_discord_clips_week
 13684  GET              /api/discord/community                           api_discord_community
 13426  GET              /api/discord/invite                              api_discord_invite
 13000  GET              /api/discord/overview                            api_discord_overview
 13086  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14211  GET              /api/events                                      api_events
 13515  GET              /api/events/stream                               api_events_stream
 14224  GET              /api/forecast/storage                            api_forecast_storage
 12013  GET              /api/freeai/status                               api_freeai_status
 12942  GET              /api/health                                      api_health
 14242  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14238  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21046  GET              /api/highlights                                  api_highlights
 21058  POST             /api/highlights/config                           api_highlights_config
 21884  GET              /api/kick/channel                                api_kick_channel
 21905  POST             /api/kick/channel                                api_kick_channel_set
 12699  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12767  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12745  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12684  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12724  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21123  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21192  POST             /api/kickmod/config                              api_kickmod_config
 21237  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21251  GET              /api/kickmod/learned                             api_kickmod_learned
 21278  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21258  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21589  POST             /api/kickmod/say                                 api_kickmod_say
 21565  POST             /api/kickmod/start                               api_kickmod_start
 21163  GET              /api/kickmod/status                              api_kickmod_status
 21576  POST             /api/kickmod/stop                                api_kickmod_stop
 10382  POST             /api/login                                       dashboard_login_submit
 14683  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14652  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13363  GET              /api/notify/status                               api_notify_status
 13374  POST             /api/notify/test                                 api_notify_test
 10606  GET              /api/outcomes                                    api_outcomes
 22504  POST             /api/overlay/config                              api_overlay_config
 22491  POST             /api/overlay/event                               api_overlay_event
 22396  GET              /api/overlay/state                               api_overlay_state
 10639  GET              /api/profile/<username>                          api_profile
 14408  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14250  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14373  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14350  GET              /api/proxy/trend                                 api_proxy_trend
 12468  GET              /api/public/stats                                api_public_stats
 10482  GET              /api/pulse                                       api_pulse
 13818  GET              /api/recording-attempts                          api_recording_attempts
 20654  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20632  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20673  POST             /api/restream/<int:rid>/start                    api_restream_start
 20944  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22358  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20608  POST             /api/restream/create                             api_restream_create
 12775  GET              /api/restream/deck                               api_restream_deck
 11949  GET              /api/restream/health                             api_restream_health
 22380  POST             /api/restream/layout                             api_restream_layout
 20581  GET              /api/restream/list                               api_restream_list
 11918  POST             /api/restream/report                             api_restream_report
 20957  POST             /api/restream/start_all                          api_restream_start_all
 20983  POST             /api/restream/stop_all                           api_restream_stop_all
 12124  GET              /api/restream/testpush                           api_testpush_status
 12149  POST             /api/restream/testpush                           api_testpush_run
 14783  GET              /api/restream/verify                             api_restream_verify
 13446  GET              /api/retention/preview                           api_retention_preview
 13455  POST             /api/retention/run                               api_retention_run
 14167  GET              /api/search                                      api_search
 23232  GET              /api/selftest                                    api_selftest
 20690  GET              /api/shield/stats                                api_shield_stats
 10543  GET              /api/storage                                     api_storage
 10550  POST             /api/storage/cleanup                             api_storage_cleanup
 14304  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11888  GET              /api/stream/timeline                             api_stream_timeline
 13074  GET              /api/stream/transcript                           api_stream_transcript
 10574  GET              /api/summary/preview                             api_summary_preview
 13883  GET              /api/system                                      api_system
 14731  GET              /api/system/check_timing                         api_check_timing
 15054  GET              /api/system/config_drift                         api_config_drift
 13110  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13221  GET              /api/system/preflight                            api_system_preflight
 13347  GET              /api/system/preflight_history                    api_system_preflight_history
 13580  GET              /api/system/resilience                           api_system_resilience
 14202  GET              /api/tags                                        api_tags_list
 10516  GET              /api/top                                         api_top
 10875  GET              /api/trend-7d                                    api_trend_7d
 21396  GET              /api/tts/<fn>                                    api_tts_file
 15026  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 14978  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15002  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 14956  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 22532  GET              /api/upload_window                               api_upload_window
 10620  GET              /api/userstats                                   api_userstats
 12516  GET              /api/version                                     api_version
 14877  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 14898  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 14910  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 14835  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 14859  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 14813  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 26922  GET              /api/youtube/sendrate                            api_youtube_sendrate
 13856  GET              /archive/<int:eid>/download                      archive_download
 13913  GET              /download/<int:recording_id>                     download
 13796  GET              /health                                          health
 20892  GET              /healthz                                         healthz
 10373  GET              /login                                           dashboard_login_page
 10403  GET              /logout                                          dashboard_logout
 10410  GET              /manifest.webmanifest                            pwa_manifest
 13138  GET              /metrics                                         api_prometheus_metrics
 22341  GET              /overlay                                         overlay_page
 10434  GET              /pwa-icon-<variant>.png                          pwa_icon
 10420  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (187)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 23937  /ai                     
 24396  /ask                    
 24028  /assign_role            
 24074  /ban                    
 24728  /botstats               
 24652  /clearwarns             
 24692  /clip                   
 24677  /clipoftheweek          
 24519  /clips                  
 23989  /create_category        
 23958  /create_channel         
 24017  /create_group           
 24000  /create_role            
 23974  /create_voice           
 24310  /daily                  
 24426  /event                  
 24469  /events                 
 24565  /follow                 
 24549  /help                   
 24063  /kick                   
 24292  /leaderboard            
 24505  /livenow                
 24535  /post_test              
 24366  /profile                
 24098  /purge                  
 24278  /rank                   
 24492  /recstatus              
 24039  /remove_role            
 23951  /restream_status        
 24050  /set_channel_perms      
 24243  /setup_community        
 24261  /setup_targets          
 24591  /stats                  
 23863  /status                 
 24887  /streaminfo             
 24784  /sys_report             
 24760  /sys_unpause            
 24085  /timeout                
 24663  /topstreamers           
 23893  /track                  
 23877  /tracklist              
 24580  /unfollow               
 23926  /untrack                
 24613  /warn                   
 24637  /warnings               
```

## Discord-Events (4)

```
 25371  on_member_join
 25333  on_message
 24974  on_raw_reaction_add
 25406  on_ready
```

## Top-Level-Symbole in bot.py (519 Funktionen, 2 Klassen)

```
  2488-2489   _abo_key
  2509-2527   _abo_probe_dump
 22774-22784  _active_recorder_sync
 17875-17882  _ad_allowlist
 18997-19003  _agent_for
 22786-22804  _ai_calls_total_sync
 19006-19022  _ai_telemetry
 19504-19522  _alert
 25522-25572  _alert_monitor_loop
 25953-26015  _announce_loop
  3430-3433   _anthropic_key
  3440-3442   _anthropic_model
 10126-10129  _arg_int
  2480-2485   _as_dict
 15735-15740  _audio_cfg
 19658-19680  _audio_tap_cmd
 10294-10305  _auth_cookie
 10261-10290  _auth_guard
  1636-1641   _auto_on
 20557-20575  _auto_restream_loop
 27083-27098  _azrael_broadcast_reply
 26983-27005  _azrael_chat_reply
 26966-26980  _azrael_chat_should_reply
 27011-27013  _azrael_gate_cfg
 19027-19041  _azrael_live_state
 22244-22258  _azrael_overlay_state
 19387-19441  _azrael_proactive_loop
 18846-18902  _azrael_reaction_to_chats
 27016-27023  _azrael_reply_all_chats
 26953-26963  _azrael_self_names
 27051-27080  _azrael_send_to
 19044-19065  _azrael_system
 25691-25694  _backup_active
 25772-25785  _backup_loop
 17763-17764  _badwords_path
 25484-25493  _brain_growth_loop
 10951-10978  _brain_growth_snapshot
  2416-2436   _brain_hint_delay
 10943-10945  _brain_history_for
  6509-6537   _brain_notify
 10920-10941  _brain_record
 10947-10949  _brain_stream_recent
 13494-13511  _browser_push
  6553-6640   _build_daily_summary
  2919-3099   _build_native_cmd
 16083-16270  _build_restream_cmd
  3143-3176   _build_ytdlp_cmd
 22726-22733  _cached_probe
  5331-5358   _can_stop_tracking
  1816-1838   _capture_set_cookies
 14467-14470  _cfg_get
 14473-14475  _cfg_set
 21988-22023  _channel_set_all
 15333-15336  _chat_connected
 15339-15355  _chat_disconnected
  8606-8617   _chat_is_forum
 15375-15377  _chat_sanitize
 15379-15388  _chat_src_ok
 15318-15330  _chat_stat
 15358-15361  _chat_stats_snapshot
  3705-3716   _check_ai_alive_sync
  3719-3731   _check_ai_models_sync
 22735-22748  _check_redis_alive_sync
 22750-22770  _check_redis_version_sync
 11550-11593  _classify_pool_anonymity
 11596-11613  _classify_pool_anonymity_bg
   794-798    _claude_chat_sync_metered
 10155-10162  _client_ip
 26047-26074  _clip_prune
 26077-26087  _clip_recfile_for
 26603-26609  _clip_should_velocity
 26128-26210  _clip_to_discord
  3603-3612   _close_ai_session
 27127-27142  _cohost_broadcast
 27109-27113  _cohost_cfg
 27168-27180  _cohost_fire_highlight
 27116-27124  _cohost_gate
 27145-27165  _cohost_highlight
 26259-26293  _community_events_loop
 10774-10776  _conv_messages
  6942-6985   _cookie_alarm_loop
  1888-1892   _cookie_autorefresh_info
  1793-1797   _cookie_header
 13544-13576  _cpu_load_snapshot
  3913-3925   _create_index_safe
 22987-23093  _crowdsec_status
 22953-22984  _crowdsec_via_lapi
 22818-22836  _cscli_bin
 22842-22855  _cscli_path
  6832-6857   _daily_summary_loop
 22873-22890  _darf_journal_lesen
 25496-25519  _db_maintenance_loop
  6801-6829   _db_vacuum_loop
 17898-17922  _detect_foreign_ad
  1374-1385   _diag_path_owner
 19293-19337  _director_finalize
 20104-20111  _director_for
 19242-19290  _director_mark
 26497-26532  _disc_automod_check
 26470-26476  _disc_state_get
 26479-26486  _disc_state_set
 23536-23549  _discord_guild_filesize_bytes
 23735-23744  _discord_invite
 26431-26467  _discord_live_thread
 19444-19456  _discord_notify
 23636-23661  _discord_ops_alert
 26329-26427  _discord_post_user
 23800-25481  _discord_run_once
 23674-23732  _discord_start
 26018-26024  _discord_stop
 23557-23559  _discord_upload_limit_label
 23552-23554  _discord_upload_limit_mb
  6860-6937   _disk_alarm_loop
 28529-28578  _disk_autoclean
 28581-28594  _disk_guard_loop
 28521-28526  _disk_pct
 15692-15694  _drawtext_chain
 14010-14012  _dump_all_threads
 11475-11539  _enrich_proxies_with_geo
  2033-2077   _ensure_cookie_file_netscape
 23747-23797  _ensure_discord_invite
 26224-26256  _ensure_error_channel
  8665-8668   _ensure_notify_topic
 11720-11757  _ensure_proxy_ready
  8619-8646   _ensure_topic
   652-654    _env_int
   657-659    _env_int_range
 26296-26326  _error_channel_loop
 19488-19501  _event_webhook
 15141-15154  _evolution_loop
  5951-5985   _extract_file_payload
  2165-2167   _extract_urls_from_streamurl_node
 22858-22865  _f2b_sudo_hint
 19524-19526  _faster_whisper_available
 17787-17799  _fetch_ldnoobw_de
 11364-11382  _fetch_proxy_list
 19938-19966  _fetch_tiktok_room_id
   728-731    _ff_cmd
 15855-15860  _find_chromium
  3136-3140   _find_external_recorder
  2170-2172   _find_stream_urls
 14518-14543  _fire_webhooks
  7721-7730   _fork_safe
   809-818    _freeai_chat_sync_metered
 22908-22950  _geo_lookup_ips
  3592-3601   _get_ai_session
  7555-7595   _get_live_info
  2706-2713   _get_resolve_semaphore
  7961-8327   _handle_single_tracking
 28373-28375  _hb
 28378-28395  _hb_while
 15393-15395  _highlight_cfg
 15398-15427  _highlight_observe
 15863-15868  _htmlov_screenshot_cmd
 19682-19692  _httpx_proxy
 14551-14563  _in_quiet_hours
 29408-29439  _install_fast_eventloop
 10021-10075  _install_fast_json
 14015-14031  _install_faulthandler
 20800-20809  _intel_ensure_schema
 20847-20882  _intel_index_loop
 20821-20831  _intel_index_one
 20812-20818  _intel_semantic
  5320-5329   _is_authorized
  7886-7892   _is_dead
  2155-2157   _is_hevc
 22893-22899  _is_private_ip
  1538-1545   _is_process_running
  6539-6550   _is_quiet_hours
  1175-1184   _is_upload_window
 10110-10123  _json_error_handler
  6759-6789   _kick_broadcaster_id
 12050-12069  _kick_channel_live
  6673-6715   _kick_follower_count
 12662-12675  _kick_oauth_exchange
 12678-12680  _kick_oauth_page
 12621-12625  _kick_redirect_public
 12616-12618  _kick_redirect_source
 12608-12613  _kick_redirect_uri
  6658-6660   _kick_slug
 12628-12659  _kick_user_token
  3962-3965   _kind_from_filename
 14580-14585  _latest_popularity
 17809-17815  _learned_load
 17806-17807  _learned_path
 17817-17825  _learned_save
 20319-20352  _live_react_loop
 20115-20308  _live_react_worker
 18905-18916  _live_transcript_push
 20310-20317  _live_users
 19340-19384  _living_title_loop
 17766-17774  _load_banned_words_file
  1714-1787   _load_cookies_dict
 25697-25769  _local_backup_scan
 10092-10106  _log_5xx
 16278-16290  _looks_like_codec_err
 16273-16275  _looks_like_source_expired
  7802-7832   _loop_fehler
 14035-14044  _loop_heartbeat
 28343-28370  _loop_lag_monitor
 14047-14115  _loop_watchdog_thread
 18785-18799  _loyalty_add
 18776-18782  _loyalty_get
 18802-18810  _loyalty_top
 14717-14719  _manual_donations_total
  7894-7895   _mark_dead
 12221-12237  _marketing_loop
 27030-27048  _maybe_handle_command
 28680-28704  _maybe_hype_clip
  3880-3903   _migrate_columns
 27307-27318  _mod_is_exempt
 27321-27326  _mod_warn_first
 27329-27332  _mod_warn_text
 15181-15189  _modlog
   928-930    _multistream_targets
  7733-7734   _nc_create_subprocess_exec
  7737-7738   _nc_create_subprocess_shell
 12473-12490  _news_loop
 15219-15221  _normalize_ingest
  2347-2364   _note_check_duration
  8659-8662   _notify_topic_name
 12572-12583  _oauth_redirect_env
 12599-12605  _oauth_redirect_source
 12586-12596  _oauth_redirect_uri
 18931-18939  _oracle_memories
 19197-19231  _oracle_memorize
 18942-18955  _oracle_persona
 18924-18928  _oracle_recent_text
 15518-15526  _ov_atomic_write
 15506-15512  _ov_bar
 17722-17734  _ov_clip_text
 15515-15516  _ov_oneline
 22308-22337  _overlay_push
 15809-15852  _overlay_render_size
 15280-15284  _overlay_session_reset
 22260-22263  _overlay_src_ok
 17885-17895  _own_invites
 15804-15806  _parse_size
 23101-23181  _parse_ssh_attacks
  7157-7190   _pause_resume_cmd
  1842-1886   _persist_refreshed_cookies
  1680-1712   _pick_checked_pull_proxy
 10191-10204  _pin_auth_value
 10250-10251  _pin_clear_fail
 10230-10233  _pin_locked
 10236-10247  _pin_note_fail
 10207-10227  _pin_ok
 22150-22152  _piper_available
 22115-22137  _piper_list_voices
 22157-22182  _piper_pick_model
 22194-22241  _piper_say
 22108-22112  _piper_voice_roots
 14480-14515  _post_json_threaded
 15783-15801  _probe_video_size
  1566-1583   _proc_is_recorder
 11462-11473  _proxy_geo_cache_put
 11689-11717  _proxy_pool_refresh_loop
  1646-1677   _proxy_report_recording
 14000-14002  _prune_stall_dumps
 12531-12569  _public_base_url
 12291-12412  _public_stats
 19459-19485  _push_notify
 10352-10354  _pwa_dir
 11433-11448  _quick_validate_proxy
 14546-14548  _quiet_hours_config
 10317-10350  _rate_guard
 18750-18756  _react_warn
  7641-7680   _reap_proc
  2387-2409   _record_check_outcome
   723-725    _redact_stream_urls
 11616-11686  _refresh_proxy_pool
 22140-22146  _resolve_piper_model
  2181-2271   _resolve_via_html
  2529-2683   _resolve_via_webcast_api_v2
  2746-2808   _resolve_via_ytdlp
 26649-26778  _resolve_youtube_ingest
 20391-20398  _restream_active_platforms
 15265-15276  _restream_active_sources
 19969-20068  _restream_chat_guardian
 15430-15502  _restream_chat_push
 15192-15204  _restream_enabled
 15871-15958  _restream_html_overlay_start
 15961-15974  _restream_html_overlay_stop
  1123-1125   _restream_layout_mode
 15230-15253  _restream_overlay_files
 20356-20388  _restream_platform_state
 20519-20554  _restream_resume_after_restart
 16022-16080  _restream_tts_enqueue_wav
 15745-15777  _restream_tts_feeder
 15742-15743  _restream_tts_fifo_path
 15977-16004  _restream_tts_start
 16006-16020  _restream_tts_stop
 20401-20516  _restream_verify_loop
 25662-25674  _retention_loop
 25621-25659  _retention_scan
  2491-2493   _room_is_abo
  5989-6106   _run_ai_call
 14138-14151  _run_async_from_flask
 22902-22905  _run_priv
 29396-29404  _run_selfcheck_and_exit
 25677-25688  _s3_client
  7897-7948   _safe_send
  4584-4600   _sample_net_throughput
 17776-17784  _save_banned_words_file
  2439-2466   _schedule_next_check
 25575-25618  _scheduler_loop
  3906-3910   _schema_pk
 14155-14160  _scraper_session
 27335-27374  _screen_full
 12958-12995  _sec_headers
  2160-2162   _select_stream_from_data_section
 29209-29393  _selfcheck
  8671-8705   _send_live_notice
  1198-1202   _should_defer_upload
 26090-26125  _shrink_for_discord
 10357-10369  _sicheres_ziel
 28601-28618  _sign_health_check
 28621-28640  _sign_health_loop
  7750-7761   _spawn
  7764-7794   _spawn_from_flask
 23225-23228  _st_befund
 19694-19935  _start_chat_listener
 14118-14135  _start_loop_watchdog
 12436-12464  _stats_loop
 12415-12418  _stats_output_path
 12421-12433  _stats_write
  8399-8415   _storage_cleanup_loop
 28660-28667  _story_for
  3198-3204   _stream_url_expiry
  3213-3219   _stream_url_is_fresh
  3206-3211   _stream_url_ttl
 17849-17856  _streamer_persona_get
 17831-17837  _streamer_personas_load
 17828-17829  _streamer_personas_path
 17839-17847  _streamer_personas_save
 15697-15701  _studio_chain
 25794-25916  _system_backup
 25919-25949  _system_backup_loop
 11385-11424  _test_proxy
 12091-12100  _testpush_cfg
 12103-12120  _testpush_exec
 12072-12088  _testpush_resolve_live
  8578-8588   _tg_topics_load_into_mem
  8575-8576   _tg_topics_path
  8590-8597   _tg_topics_save
 10165-10173  _token_ok
  8600-8604   _topic_forget
 14566-14577  _tracking_max_duration
  4171-4185   _tracking_remove_cleanup
  4202-4214   _tracking_resume_cleanup
  1432-1455   _try_attach_file_handler
 22184-22192  _tts_cleanup
 12028-12032  _tunnel_effective
 21610-21663  _twitch_channel_status
 27377-27520  _twitch_chat_loop
 27191-27294  _twitch_eventsub_loop
 15047-15050  _twitch_oauth_page
  1221-1234   _upload_queue_add
  1245-1247   _upload_queue_count
  1204-1213   _upload_queue_load
  1194-1196   _upload_queue_path
  1236-1243   _upload_queue_remove
  1215-1219   _upload_queue_save
  1249-1290   _upload_window_loop
  7614-7621   _uptime_s
 15207-15216  _url_host
   703-720    _url_ohne_zugang
   787-791    _usage_record_claude
  7835-7879   _verbindung_verloren
  6718-6749   _viewer_sample_loop
  6791-6798   _viewer_stats
 10254-10257  _wants_html
  7624-7638   _warn_empty_env
 28416-28511  _watchdog_loop
 26932-26940  _wchat_thank_ok
 19528-19558  _whisper_get_model
  7711-7718   _whisper_native_section
 18737-18743  _whisper_pool
 19627-19656  _whisper_segments
 19560-19624  _whisper_transcribe
 15528-15690  _write_restream_overlay
 27548-27627  _youtube_api_chat_loop
 21666-21769  _youtube_api_status
 21772-21839  _youtube_channel_status
 27630-27790  _youtube_chat_loop
 26784-26797  _youtube_restream_autoconfig
 26800-26824  _youtube_restream_autoconfig_inner
 26890-26918  _youtube_send
 21944-21985  _youtube_set_channel
 26827-26861  _yt_access_token
 26864-26879  _yt_live_chat_id
 27541-27545  _yt_oauth_configured
 26885-26887  _yt_sendrate_cfg
 27523-27538  _yt_timeout
  2730-2731   _ytdlp_detect_available
  2733-2744   _ytdlp_note_result
 14005-14007  _zombie_child_count
  7491-7515   about
  4081-4085   add_ai_log_entry
  3998-4001   add_archive_entry
  4697-4712   add_archive_rule
  4373-4407   add_recording
  4146-4163   add_tracking
  6109-6142   ai
  3745-3784   ai_chat
  3818-3828   ai_history_append
  3830-3835   ai_history_clear
  3807-3816   ai_history_load
  3792-3805   ai_rate_limit_check
  6171-6179   aireset
 19068-19087  azrael_chat
 27795-27917  brain_cmd
  3222-3406   build_recording_cmd
  4166-4169   bulk_add_trackings
  6988-7047   bulkadd
  8418-8558   check_all_trackings
  4218-4230   claim_live_transition
 17925-18680  class KickModerator
 16293-17609  class RestreamManager
 11802-11844  classify_proxy_anonymity
  6217-6415   cleanup
  5180-5221   cleanup_old_recordings
  4364-4371   clear_recording
 26535-26600  clip_moment
  4528-4577   compute_storage_forecast
  7110-7154   cookies_cmd
  4137-4143   count_trackings_for_chat
  4068-4079   decide_preferred_recorder
  4008-4011   delete_archive_entry
  4714-4722   delete_archive_rule
  5646-5793   diag
 28029-28090  einnahmen_cmd
  4522-4525   find_recordings_by_fingerprint
  4029-4045   finish_recording_attempt
  4190-4192   get_all_active_trackings
  4096-4099   get_all_checks
  4409-4412   get_all_recordings
  4471-4473   get_all_tags_with_counts
  4499-4502   get_annotations_for_recording
  4003-4006   get_archive_entry
  4492-4495   get_bookmarked_recordings
  1909-2026   get_cookie_health
  4459-4465   get_event_log
  4052-4066   get_last_recording_attempt
  2811-2916   get_live_status
  4980-4983   get_manual_recordings
  4507-4510   get_or_compute_inspect_sync
  5256-5300   get_outcome_breakdown
  4478-4481   get_priority_poll_interval
  4675-4684   get_profile_snapshots
  4047-4050   get_recent_recording_attempts
  4414-4417   get_recording_by_id
  4485-4488   get_recording_note
  3540-3563   get_redis
  4126-4129   get_stats
  5147-5178   get_storage_stats
  4815-4817   get_tiktok_status_distribution
  4232-4241   get_tracking_state
  4187-4188   get_trackings_for_group
  4996-4999   get_trash_recordings
  9326-9989   handle_recording_finished
  3928-3953   init_db
  5070-5124   inspect_stream_url
 22303-22305  is_revenue_platform
  4687-4695   list_archive_rules
  5450-5488   live
  7951-7959   live_check_worker
  3615-3649   llm_chat
  3672-3700   llm_chat_sync
  3657-3669   llm_list_models
  4425-4451   log_event
  1500-1533   log_recording_failure
  7304-7353   logs_cmd
 28708-29199  main
  6145-6168   on_ai_media
  7430-7456   on_ai_reply
  7459-7488   on_azrael_mention
  7520-7550   on_callback
 19090-19194  oracle_handle
  7193-7196   pause_tracking
  5310-5315   profile_keyboard
  7255-7301   quota
  8329-8396   reaper_loop
  4811-4813   record_tiktok_status
  6184-6214   recstatus
  3565-3573   redis_get_json
  3575-3581   redis_set_json
 28093-28103  report_cmd
 11847-11849  report_proxy_result
  2274-2301   resolve_tiktok_live_stream
  4991-4994   restore_recording
  7199-7202   resume_tracking
  4725-4805   run_archive_rules
 28106-28323  run_bot
 13927-13974  run_flask
  4603-4648   sample_bandwidth_for_active
  4654-4673   save_profile_snapshot
  4088-4094   save_tiktok_check
  4356-4362   set_recording_file
  4195-4199   set_tracking_paused
  4986-4989   soft_delete_recording
  8711-9324   split_and_send_video
  5363-5405   start
  4013-4027   start_recording_attempt
  6418-6456   stats
  4961-4978   stop_manual_recording
  7205-7252   stoprec
  6643-6651   summary_cmd
  7356-7427   sysres
  5795-5939   teststream
  5407-5448   tiktok
  7050-7107   topusers
  5525-5582   track
  5490-5522   track_exact
  5596-5644   tracklist
  4827-4959   trigger_manual_recording
  4317-4354   try_acquire_recording_lock
  5002-5061   universal_search
  5584-5594   untrack
 27920-28026  update_cmd
  4517-4520   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aus_accept_language, configure, katalog, normalisieren, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
