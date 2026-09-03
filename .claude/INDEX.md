# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (111)

```
 10481  GET              /                                                dashboard
 13872  GET              /api/abo/status                                  api_abo_status
 10554  GET              /api/active-recordings                           api_active_recordings
 13943  GET              /api/activity-pulse                              api_activity_pulse
 13750  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 13816  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13840  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13844  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11990  GET              /api/automation/status                           api_automation_status
 12012  POST             /api/automation/toggle                           api_automation_toggle
 10853  GET              /api/backoff-watch                               api_backoff_watch
 13312  POST             /api/backup/run                                  api_backup_run
 13278  GET              /api/backup/status                               api_backup_status
 13267  POST             /api/backup/system                               api_backup_system
 13782  GET              /api/bandwidth/live                              api_bandwidth_live
 13735  GET              /api/bookmarks                                   api_bookmarks_list
 11116  GET              /api/brain                                       api_brain
 11053  GET              /api/brain/alarms                                api_brain_alarms
 11038  GET              /api/brain/creator                               api_brain_creator
 11015  GET              /api/brain/graph                                 api_brain_graph
 11076  GET              /api/brain/growth                                api_brain_growth
 10031  GET              /api/brain/health                                api_brain_health
 20881  GET              /api/channel/categories                          api_channel_categories
 20887  POST             /api/channel/set                                 api_channel_set
 20734  GET              /api/channels/status                             api_channels_status
 10535  GET              /api/checks                                      api_checks
 20408  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20391  GET              /api/clips                                       api_clips
 20437  POST/DELETE      /api/clips/clear                                 api_clips_clear
 14251  GET              /api/community/stats                             api_community_stats
 21352  GET              /api/data/export                                 api_data_export
 20260  GET              /api/debug/threads                               api_debug_threads
 22199  GET              /api/defense/attacks                             api_defense_attacks
 22166  GET              /api/defense/crowdsec                            api_defense_crowdsec
 22184  GET              /api/defense/fail2ban                            api_defense_fail2ban
 21890  GET              /api/defense/overview                            api_defense_overview
 13764  GET              /api/events                                      api_events
 13149  GET              /api/events/stream                               api_events_stream
 13777  GET              /api/forecast/storage                            api_forecast_storage
 12028  GET              /api/freeai/status                               api_freeai_status
 12738  GET              /api/health                                      api_health
 13795  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13791  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20338  GET              /api/highlights                                  api_highlights
 20350  POST             /api/highlights/config                           api_highlights_config
 10415  POST             /api/login                                       dashboard_login_submit
 14236  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14205  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13047  GET              /api/notify/status                               api_notify_status
 13058  POST             /api/notify/test                                 api_notify_test
 10639  GET              /api/outcomes                                    api_outcomes
 10672  GET              /api/profile/<username>                          api_profile
 13961  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13803  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13926  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13903  GET              /api/proxy/trend                                 api_proxy_trend
 12483  GET              /api/public/stats                                api_public_stats
 10515  GET              /api/pulse                                       api_pulse
 13371  GET              /api/recording-attempts                          api_recording_attempts
 20062  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20040  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20081  POST             /api/restream/<int:rid>/start                    api_restream_start
 20281  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21173  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20016  POST             /api/restream/create                             api_restream_create
 12608  GET              /api/restream/deck                               api_restream_deck
 11964  GET              /api/restream/health                             api_restream_health
 21195  POST             /api/restream/layout                             api_restream_layout
 19989  GET              /api/restream/list                               api_restream_list
 11933  POST             /api/restream/report                             api_restream_report
 20294  POST             /api/restream/start_all                          api_restream_start_all
 20320  POST             /api/restream/stop_all                           api_restream_stop_all
 12139  GET              /api/restream/testpush                           api_testpush_status
 12164  POST             /api/restream/testpush                           api_testpush_run
 14336  GET              /api/restream/verify                             api_restream_verify
 13096  GET              /api/retention/preview                           api_retention_preview
 13105  POST             /api/retention/run                               api_retention_run
 13720  GET              /api/search                                      api_search
 21937  GET              /api/selftest                                    api_selftest
 20098  GET              /api/shield/stats                                api_shield_stats
 10576  GET              /api/storage                                     api_storage
 10583  POST             /api/storage/cleanup                             api_storage_cleanup
 13857  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11903  GET              /api/stream/timeline                             api_stream_timeline
 12799  GET              /api/stream/transcript                           api_stream_transcript
 10607  GET              /api/summary/preview                             api_summary_preview
 13436  GET              /api/system                                      api_system
 14284  GET              /api/system/check_timing                         api_check_timing
 14399  GET              /api/system/config_drift                         api_config_drift
 12813  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12905  GET              /api/system/preflight                            api_system_preflight
 13031  GET              /api/system/preflight_history                    api_system_preflight_history
 13214  GET              /api/system/resilience                           api_system_resilience
 13755  GET              /api/tags                                        api_tags_list
 10549  GET              /api/top                                         api_top
 10908  GET              /api/trend-7d                                    api_trend_7d
 20457  GET              /api/tts/<fn>                                    api_tts_file
 21217  GET              /api/upload_window                               api_upload_window
 10653  GET              /api/userstats                                   api_userstats
 12531  GET              /api/version                                     api_version
 13409  GET              /archive/<int:eid>/download                      archive_download
 13466  GET              /download/<int:recording_id>                     download
 13349  GET              /health                                          health
 20229  GET              /healthz                                         healthz
 10406  GET              /login                                           dashboard_login_page
 10436  GET              /logout                                          dashboard_logout
 10443  GET              /manifest.webmanifest                            pwa_manifest
 12841  GET              /metrics                                         api_prometheus_metrics
 21156  GET              /overlay                                         overlay_page
 10467  GET              /pwa-icon-<variant>.png                          pwa_icon
 10453  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (248)

```
   185  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   155  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   994  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   734  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   865  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   845  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   883  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   807  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   347  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   358  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   368  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   391  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   398  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   409  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   542  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   640  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1232  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1264  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   331  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   947  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   927  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1100  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1148  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1199  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1058  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   902  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   366  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   630  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   512  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   495  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   487  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   323  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   339  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   674  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   639  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   659  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   546  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    40  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    69  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   235  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   161  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   179  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   151  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    54  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   127  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    70  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   103  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   111  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    51  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   127  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   156  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   141  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    81  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   103  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   124  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    71  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   171  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    35  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   191  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   211  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   238  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   211  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   210  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   232  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    91  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   159  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   137  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    76  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   116  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   166  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   215  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   258  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   325  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   353  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   204  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   271  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   506  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    71  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   169  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   152  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   392  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   485  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   480  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   528  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   411  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   738  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   465  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   438  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   712  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   582  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   671  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   577  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   510  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   290  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   755  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   378  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   633  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   788  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   773  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   334  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   572  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   558  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   541  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   598  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   691  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   587  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   117  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   264  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    79  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   289  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   221  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   245  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   176  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   141  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   201  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    47  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   228  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   443  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   472  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   392  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   405  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   501  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   378  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   253  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   298  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   322  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   309  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   155  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   267  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   125  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   359  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   414  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   112  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    91  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   123  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   104  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   115  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    67  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    91  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    45  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   454  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   420  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   479  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   459  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   442  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   435  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    42  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    82  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   113  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    97  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   122  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   143  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   155  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    80  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   104  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    58  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   190  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 22663  /ai                     
 23122  /ask                    
 22754  /assign_role            
 22800  /ban                    
 23454  /botstats               
 23378  /clearwarns             
 23418  /clip                   
 23403  /clipoftheweek          
 23245  /clips                  
 22715  /create_category        
 22684  /create_channel         
 22743  /create_group           
 22726  /create_role            
 22700  /create_voice           
 23036  /daily                  
 23152  /event                  
 23195  /events                 
 23291  /follow                 
 23275  /help                   
 22789  /kick                   
 23018  /leaderboard            
 23231  /livenow                
 23261  /post_test              
 23092  /profile                
 22824  /purge                  
 23004  /rank                   
 23218  /recstatus              
 22765  /remove_role            
 22677  /restream_status        
 22776  /set_channel_perms      
 22969  /setup_community        
 22987  /setup_targets          
 23317  /stats                  
 22589  /status                 
 23613  /streaminfo             
 23510  /sys_report             
 23486  /sys_unpause            
 22811  /timeout                
 23389  /topstreamers           
 22619  /track                  
 22603  /tracklist              
 23306  /unfollow               
 22652  /untrack                
 23339  /warn                   
 23363  /warnings               
```

## Discord-Events (4)

```
 24099  on_member_join
 24061  on_message
 23700  on_raw_reaction_add
 24134  on_ready
```

## Top-Level-Symbole in bot.py (494 Funktionen, 2 Klassen)

```
  2510-2511   _abo_key
  2531-2549   _abo_probe_dump
 21459-21469  _active_recorder_sync
 17261-17268  _ad_allowlist
 18399-18405  _agent_for
 21471-21489  _ai_calls_total_sync
 18408-18424  _ai_telemetry
 18912-18930  _alert
 24250-24300  _alert_monitor_loop
 24681-24743  _announce_loop
  3452-3455   _anthropic_key
  3462-3464   _anthropic_model
 10159-10162  _arg_int
  2502-2507   _as_dict
 19066-19088  _audio_tap_cmd
 10327-10338  _auth_cookie
 10294-10323  _auth_guard
  1658-1663   _auto_on
 19965-19983  _auto_restream_loop
 25799-25814  _azrael_broadcast_reply
 25699-25721  _azrael_chat_reply
 25682-25696  _azrael_chat_should_reply
 25727-25729  _azrael_gate_cfg
 18429-18443  _azrael_live_state
 21068-21082  _azrael_overlay_state
 18795-18849  _azrael_proactive_loop
 18247-18303  _azrael_reaction_to_chats
 25732-25739  _azrael_reply_all_chats
 25669-25679  _azrael_self_names
 25767-25796  _azrael_send_to
 18449-18470  _azrael_system
 24419-24422  _backup_active
 24500-24513  _backup_loop
 24212-24221  _brain_growth_loop
 10984-11011  _brain_growth_snapshot
  2438-2458   _brain_hint_delay
 10976-10978  _brain_history_for
  6543-6571   _brain_notify
 10953-10974  _brain_record
 10980-10982  _brain_stream_recent
 13128-13145  _browser_push
  6587-6674   _build_daily_summary
  2941-3121   _build_native_cmd
 15449-15636  _build_restream_cmd
  3165-3198   _build_ytdlp_cmd
 21411-21418  _cached_probe
  5365-5392   _can_stop_tracking
  1838-1860   _capture_set_cookies
 14020-14023  _cfg_get
 14026-14028  _cfg_set
 20842-20877  _channel_set_all
 14683-14686  _chat_connected
 14689-14705  _chat_disconnected
  8639-8650   _chat_is_forum
 14725-14727  _chat_sanitize
 14729-14738  _chat_src_ok
 14668-14680  _chat_stat
 14708-14711  _chat_stats_snapshot
  3727-3738   _check_ai_alive_sync
  3741-3753   _check_ai_models_sync
 21420-21433  _check_redis_alive_sync
 21435-21455  _check_redis_version_sync
 11583-11626  _classify_pool_anonymity
 11629-11646  _classify_pool_anonymity_bg
   816-820    _claude_chat_sync_metered
 10188-10195  _client_ip
 24775-24802  _clip_prune
 24805-24815  _clip_recfile_for
 25328-25334  _clip_should_velocity
 24856-24938  _clip_to_discord
  3625-3634   _close_ai_session
 25845-25860  _cohost_broadcast
 25830-25831  _cohost_cfg
 25886-25898  _cohost_fire_highlight
 25834-25842  _cohost_gate
 25863-25883  _cohost_highlight
 24987-25021  _community_events_loop
 10807-10809  _conv_messages
  6951-6994   _cookie_alarm_loop
  1910-1914   _cookie_autorefresh_info
  1815-1819   _cookie_header
 13178-13210  _cpu_load_snapshot
  3947-3959   _create_index_safe
 21692-21798  _crowdsec_status
 21638-21689  _crowdsec_via_lapi
 21503-21521  _cscli_bin
 21527-21540  _cscli_path
  6841-6866   _daily_summary_loop
 21558-21575  _darf_journal_lesen
 24224-24247  _db_maintenance_loop
  6810-6838   _db_vacuum_loop
 17284-17308  _detect_foreign_ad
  1396-1407   _diag_path_owner
 18701-18745  _director_finalize
 19512-19519  _director_for
 18650-18698  _director_mark
 25222-25257  _disc_automod_check
 25198-25201  _disc_state_get
 25204-25211  _disc_state_set
 22241-22254  _discord_guild_filesize_bytes
 22446-22450  _discord_invite
 25159-25195  _discord_live_thread
 18852-18864  _discord_notify
 22345-22370  _discord_ops_alert
 25057-25155  _discord_post_user
 22506-24209  _discord_run_once
 22385-22443  _discord_start
 24746-24752  _discord_stop
 22262-22264  _discord_upload_limit_label
 22257-22259  _discord_upload_limit_mb
  6869-6946   _disk_alarm_loop
 27282-27331  _disk_autoclean
 27334-27347  _disk_guard_loop
 27274-27279  _disk_pct
 15042-15044  _drawtext_chain
 13563-13565  _dump_all_threads
 11508-11572  _enrich_proxies_with_geo
  2055-2099   _ensure_cookie_file_netscape
 22453-22503  _ensure_discord_invite
 24952-24984  _ensure_error_channel
  8698-8701   _ensure_notify_topic
 11753-11790  _ensure_proxy_ready
  8652-8679   _ensure_topic
   673-675    _env_int
   678-680    _env_int_range
 25024-25054  _error_channel_loop
 18896-18909  _event_webhook
 14486-14499  _evolution_loop
  5985-6019   _extract_file_payload
  2187-2189   _extract_urls_from_streamurl_node
 21543-21550  _f2b_sudo_hint
 18932-18934  _faster_whisper_available
 11397-11415  _fetch_proxy_list
 19346-19374  _fetch_tiktok_room_id
   749-752    _ff_cmd
 15208-15213  _find_chromium
  3158-3162   _find_external_recorder
  2192-2194   _find_stream_urls
 14071-14096  _fire_webhooks
  7730-7739   _fork_safe
   831-840    _freeai_chat_sync_metered
 21593-21635  _geo_lookup_ips
  3614-3623   _get_ai_session
  7564-7604   _get_live_info
  2728-2735   _get_resolve_semaphore
  7994-8360   _handle_single_tracking
 27100-27102  _hb
 27105-27122  _hb_while
 14743-14745  _highlight_cfg
 14748-14777  _highlight_observe
 15216-15234  _htmlov_screenshot_cmd
 19090-19100  _httpx_proxy
 14104-14116  _in_quiet_hours
 28173-28204  _install_fast_eventloop
 10054-10108  _install_fast_json
 13568-13584  _install_faulthandler
 20137-20146  _intel_ensure_schema
 20184-20219  _intel_index_loop
 20158-20168  _intel_index_one
 20149-20155  _intel_semantic
  5354-5363   _is_authorized
  7895-7901   _is_dead
  2177-2179   _is_hevc
 21578-21584  _is_private_ip
  1560-1567   _is_process_running
  6573-6584   _is_quiet_hours
  1197-1206   _is_upload_window
 10143-10156  _json_error_handler
  6796-6797   _kick_broadcaster_id
 12065-12084  _kick_channel_live
  6708-6750   _kick_follower_count
  6692-6695   _kick_slug
 12558-12589  _kick_user_token
  3996-3999   _kind_from_filename
 14133-14138  _latest_popularity
 19727-19760  _live_react_loop
 19523-19716  _live_react_worker
 18306-18317  _live_transcript_push
 19718-19725  _live_users
 18748-18792  _living_title_loop
  1736-1809   _load_cookies_dict
 24425-24497  _local_backup_scan
 10125-10139  _log_5xx
 15644-15656  _looks_like_codec_err
 15639-15641  _looks_like_source_expired
  7811-7841   _loop_fehler
 13588-13597  _loop_heartbeat
 27070-27097  _loop_lag_monitor
 13600-13668  _loop_watchdog_thread
 18186-18200  _loyalty_add
 18177-18183  _loyalty_get
 18203-18211  _loyalty_top
 14270-14272  _manual_donations_total
  7903-7904   _mark_dead
 12236-12252  _marketing_loop
 25746-25764  _maybe_handle_command
 27433-27457  _maybe_hype_clip
  3914-3937   _migrate_columns
 26025-26036  _mod_is_exempt
 26039-26044  _mod_warn_first
 26047-26050  _mod_warn_text
 14526-14534  _modlog
   950-952    _multistream_targets
  7742-7743   _nc_create_subprocess_exec
  7746-7747   _nc_create_subprocess_shell
 12488-12505  _news_loop
 14564-14566  _normalize_ingest
  2369-2386   _note_check_duration
  8692-8695   _notify_topic_name
 18332-18340  _oracle_memories
 18605-18639  _oracle_memorize
 18343-18356  _oracle_persona
 18325-18329  _oracle_recent_text
 14868-14876  _ov_atomic_write
 14856-14862  _ov_bar
 17187-17199  _ov_clip_text
 14865-14866  _ov_oneline
 21120-21149  _overlay_push
 15162-15205  _overlay_render_size
 14630-14634  _overlay_session_reset
 21084-21087  _overlay_src_ok
 17271-17281  _own_invites
 15157-15159  _parse_size
 21806-21886  _parse_ssh_attacks
  7166-7199   _pause_resume_cmd
  1864-1908   _persist_refreshed_cookies
  1702-1734   _pick_checked_pull_proxy
 10224-10237  _pin_auth_value
 10283-10284  _pin_clear_fail
 10263-10266  _pin_locked
 10269-10280  _pin_note_fail
 10240-10260  _pin_ok
 20978-21003  _piper_pick_model
 21015-21062  _piper_say
 14033-14068  _post_json_threaded
 15136-15154  _probe_video_size
  1588-1605   _proc_is_recorder
 11495-11506  _proxy_geo_cache_put
 11722-11750  _proxy_pool_refresh_loop
  1668-1699   _proxy_report_recording
 13553-13555  _prune_stall_dumps
 12306-12427  _public_stats
 18867-18893  _push_notify
 10385-10387  _pwa_dir
 11466-11481  _quick_validate_proxy
 14099-14101  _quiet_hours_config
 10350-10383  _rate_guard
 18151-18157  _react_warn
  7650-7689   _reap_proc
  2409-2431   _record_check_outcome
   744-746    _redact_stream_urls
 11649-11719  _refresh_proxy_pool
  2203-2293   _resolve_via_html
  2551-2705   _resolve_via_webcast_api_v2
  2768-2830   _resolve_via_ytdlp
 25373-25502  _resolve_youtube_ingest
 19799-19806  _restream_active_platforms
 14613-14624  _restream_active_sources
 19377-19476  _restream_chat_guardian
 14780-14852  _restream_chat_push
 14537-14549  _restream_enabled
 15237-15324  _restream_html_overlay_start
 15327-15340  _restream_html_overlay_stop
  1145-1147   _restream_layout_mode
 14575-14598  _restream_overlay_files
 19764-19796  _restream_platform_state
 19927-19962  _restream_resume_after_restart
 15388-15446  _restream_tts_enqueue_wav
 15098-15130  _restream_tts_feeder
 15095-15096  _restream_tts_fifo_path
 15343-15370  _restream_tts_start
 15372-15386  _restream_tts_stop
 19809-19924  _restream_verify_loop
 24390-24402  _retention_loop
 24349-24387  _retention_scan
  2513-2515   _room_is_abo
  6023-6140   _run_ai_call
 13691-13704  _run_async_from_flask
 21587-21590  _run_priv
 28161-28169  _run_selfcheck_and_exit
 24405-24416  _s3_client
  7930-7981   _safe_send
  4618-4634   _sample_net_throughput
  2461-2488   _schedule_next_check
 24303-24346  _scheduler_loop
  3940-3944   _schema_pk
 13708-13713  _scraper_session
 26053-26092  _screen_full
 12754-12791  _sec_headers
  2182-2184   _select_stream_from_data_section
 27974-28158  _selfcheck
  8704-8738   _send_live_notice
  1220-1224   _should_defer_upload
 24818-24853  _shrink_for_discord
 10390-10402  _sicheres_ziel
 27354-27371  _sign_health_check
 27374-27393  _sign_health_loop
  7759-7770   _spawn
  7773-7803   _spawn_from_flask
 21930-21933  _st_befund
 19102-19343  _start_chat_listener
 13671-13688  _start_loop_watchdog
 12451-12479  _stats_loop
 12430-12433  _stats_output_path
 12436-12448  _stats_write
  8432-8448   _storage_cleanup_loop
 27413-27420  _story_for
  3220-3226   _stream_url_expiry
  3235-3241   _stream_url_is_fresh
  3228-3233   _stream_url_ttl
 17234-17241  _streamer_persona_get
 15047-15051  _studio_chain
 24522-24644  _system_backup
 24647-24677  _system_backup_loop
 11418-11457  _test_proxy
 12106-12115  _testpush_cfg
 12118-12135  _testpush_exec
 12087-12103  _testpush_resolve_live
  7906-7927   _tg_sprache_setzen
  8611-8621   _tg_topics_load_into_mem
  8608-8609   _tg_topics_path
  8623-8630   _tg_topics_save
 10198-10206  _token_ok
  8633-8637   _topic_forget
 14119-14130  _tracking_max_duration
  4205-4219   _tracking_remove_cleanup
  4236-4248   _tracking_resume_cleanup
  1454-1477   _try_attach_file_handler
 21005-21013  _tts_cleanup
 12043-12047  _tunnel_effective
 20501-20554  _twitch_channel_status
 26095-26240  _twitch_chat_loop
 25909-26012  _twitch_eventsub_loop
  1243-1256   _upload_queue_add
  1267-1269   _upload_queue_count
  1226-1235   _upload_queue_load
  1216-1218   _upload_queue_path
  1258-1265   _upload_queue_remove
  1237-1241   _upload_queue_save
  1271-1312   _upload_window_loop
  7623-7630   _uptime_s
 14552-14561  _url_host
   724-741    _url_ohne_zugang
   809-813    _usage_record_claude
  7844-7888   _verbindung_verloren
  6753-6784   _viewer_sample_loop
  6800-6807   _viewer_stats
 10287-10290  _wants_html
  7633-7647   _warn_empty_env
 27143-27264  _watchdog_loop
 25648-25656  _wchat_thank_ok
 18936-18966  _whisper_get_model
  7720-7727   _whisper_native_section
 18138-18144  _whisper_pool
 19035-19064  _whisper_segments
 18968-19032  _whisper_transcribe
 14878-15040  _write_restream_overlay
 26268-26348  _youtube_api_chat_loop
 20557-20660  _youtube_api_status
 20663-20730  _youtube_channel_status
 26351-26512  _youtube_chat_loop
 25508-25521  _youtube_restream_autoconfig
 25524-25548  _youtube_restream_autoconfig_inner
 25615-25643  _youtube_send
 20798-20839  _youtube_set_channel
 25551-25585  _yt_access_token
 25588-25603  _yt_live_chat_id
 26261-26265  _yt_oauth_configured
 25611-25612  _yt_sendrate_cfg
 26243-26258  _yt_timeout
  2752-2753   _ytdlp_detect_available
  2755-2766   _ytdlp_note_result
 13558-13560  _zombie_child_count
  7500-7524   about
  4115-4119   add_ai_log_entry
  4032-4035   add_archive_entry
  4731-4746   add_archive_rule
  4407-4441   add_recording
  4180-4197   add_tracking
  6143-6176   ai
  3767-3818   ai_chat
  3852-3862   ai_history_append
  3864-3869   ai_history_clear
  3841-3850   ai_history_load
  3826-3839   ai_rate_limit_check
  6205-6213   aireset
 18473-18492  azrael_chat
 26517-26639  brain_cmd
  3244-3428   build_recording_cmd
  4200-4203   bulk_add_trackings
  6997-7056   bulkadd
  8451-8591   check_all_trackings
  4252-4264   claim_live_transition
 17311-18073  class KickModerator
 15659-17074  class RestreamManager
 11835-11877  classify_proxy_anonymity
  6251-6449   cleanup
  5214-5255   cleanup_old_recordings
  4398-4405   clear_recording
 25260-25325  clip_moment
  4562-4611   compute_storage_forecast
  7119-7163   cookies_cmd
  4171-4177   count_trackings_for_chat
  4102-4113   decide_preferred_recorder
  4042-4045   delete_archive_entry
  4748-4756   delete_archive_rule
  5680-5827   diag
 26751-26812  einnahmen_cmd
  4556-4559   find_recordings_by_fingerprint
  4063-4079   finish_recording_attempt
  4224-4226   get_all_active_trackings
  4130-4133   get_all_checks
  4443-4446   get_all_recordings
  4505-4507   get_all_tags_with_counts
  4533-4536   get_annotations_for_recording
  4037-4040   get_archive_entry
  4526-4529   get_bookmarked_recordings
  1931-2048   get_cookie_health
  4493-4499   get_event_log
  4086-4100   get_last_recording_attempt
  2833-2938   get_live_status
  5014-5017   get_manual_recordings
  4541-4544   get_or_compute_inspect_sync
  5290-5334   get_outcome_breakdown
  4512-4515   get_priority_poll_interval
  4709-4718   get_profile_snapshots
  4081-4084   get_recent_recording_attempts
  4448-4451   get_recording_by_id
  4519-4522   get_recording_note
  3562-3585   get_redis
  4160-4163   get_stats
  5181-5212   get_storage_stats
  4849-4851   get_tiktok_status_distribution
  4266-4275   get_tracking_state
  4221-4222   get_trackings_for_group
  5030-5033   get_trash_recordings
  9359-10022  handle_recording_finished
  3962-3987   init_db
  5104-5158   inspect_stream_url
  4721-4729   list_archive_rules
  5484-5522   live
  7984-7992   live_check_worker
  3637-3671   llm_chat
  3694-3722   llm_chat_sync
  3679-3691   llm_list_models
  4459-4485   log_event
  1522-1555   log_recording_failure
  7313-7362   logs_cmd
 27461-27964  main
  6179-6202   on_ai_media
  7439-7465   on_ai_reply
  7468-7497   on_azrael_mention
  7529-7559   on_callback
 18498-18602  oracle_handle
  7202-7205   pause_tracking
  5344-5349   profile_keyboard
  7264-7310   quota
  8362-8429   reaper_loop
  4845-4847   record_tiktok_status
  6218-6248   recstatus
  3587-3595   redis_get_json
  3597-3603   redis_set_json
 26815-26825  report_cmd
 11880-11882  report_proxy_result
  2296-2323   resolve_tiktok_live_stream
  5025-5028   restore_recording
  7208-7211   resume_tracking
  4759-4839   run_archive_rules
 26828-27050  run_bot
 13480-13527  run_flask
  4637-4682   sample_bandwidth_for_active
  4688-4707   save_profile_snapshot
  4122-4128   save_tiktok_check
  4390-4396   set_recording_file
  4229-4233   set_tracking_paused
  5020-5023   soft_delete_recording
  8744-9357   split_and_send_video
  5397-5439   start
  4047-4061   start_recording_attempt
  6452-6490   stats
  4995-5012   stop_manual_recording
  7214-7261   stoprec
  6677-6685   summary_cmd
  7365-7436   sysres
  5829-5973   teststream
  5441-5482   tiktok
  7059-7116   topusers
  5559-5616   track
  5524-5556   track_exact
  5630-5678   tracklist
  4861-4993   trigger_manual_recording
  4351-4388   try_acquire_recording_lock
  5036-5095   universal_search
  5618-5628   untrack
 26642-26748  update_cmd
  4551-4554   update_recording_fingerprint
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
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
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
discordstate.py        invite, state_get
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
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
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
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restrend.py            rising_trend
revenue.py             is_revenue_platform, normalisieren, sql_in
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
util.py                datei_in
version.py             changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
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
