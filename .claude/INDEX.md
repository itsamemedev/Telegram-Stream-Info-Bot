# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (105)

```
 10472  GET              /                                                dashboard
 13537  GET              /api/abo/status                                  api_abo_status
 10545  GET              /api/active-recordings                           api_active_recordings
 13608  GET              /api/activity-pulse                              api_activity_pulse
 13415  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 13481  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13505  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13509  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11653  GET              /api/automation/status                           api_automation_status
 11675  POST             /api/automation/toggle                           api_automation_toggle
 10844  GET              /api/backoff-watch                               api_backoff_watch
 12975  POST             /api/backup/run                                  api_backup_run
 12941  GET              /api/backup/status                               api_backup_status
 12930  POST             /api/backup/system                               api_backup_system
 13447  GET              /api/bandwidth/live                              api_bandwidth_live
 13400  GET              /api/bookmarks                                   api_bookmarks_list
 20546  GET              /api/channel/categories                          api_channel_categories
 20552  POST             /api/channel/set                                 api_channel_set
 20399  GET              /api/channels/status                             api_channels_status
 10526  GET              /api/checks                                      api_checks
 20073  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20056  GET              /api/clips                                       api_clips
 20102  POST/DELETE      /api/clips/clear                                 api_clips_clear
 13916  GET              /api/community/stats                             api_community_stats
 21017  GET              /api/data/export                                 api_data_export
 19925  GET              /api/debug/threads                               api_debug_threads
 21864  GET              /api/defense/attacks                             api_defense_attacks
 21831  GET              /api/defense/crowdsec                            api_defense_crowdsec
 21849  GET              /api/defense/fail2ban                            api_defense_fail2ban
 21555  GET              /api/defense/overview                            api_defense_overview
 13429  GET              /api/events                                      api_events
 12812  GET              /api/events/stream                               api_events_stream
 13442  GET              /api/forecast/storage                            api_forecast_storage
 11691  GET              /api/freeai/status                               api_freeai_status
 12401  GET              /api/health                                      api_health
 13460  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13456  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20003  GET              /api/highlights                                  api_highlights
 20015  POST             /api/highlights/config                           api_highlights_config
 10406  POST             /api/login                                       dashboard_login_submit
 13901  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13870  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12710  GET              /api/notify/status                               api_notify_status
 12721  POST             /api/notify/test                                 api_notify_test
 10630  GET              /api/outcomes                                    api_outcomes
 10663  GET              /api/profile/<username>                          api_profile
 13626  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13468  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13591  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13568  GET              /api/proxy/trend                                 api_proxy_trend
 12146  GET              /api/public/stats                                api_public_stats
 10506  GET              /api/pulse                                       api_pulse
 13034  GET              /api/recording-attempts                          api_recording_attempts
 19727  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 19705  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 19746  POST             /api/restream/<int:rid>/start                    api_restream_start
 19946  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 20838  GET              /api/restream/chatfeed                           api_restream_chatfeed
 19681  POST             /api/restream/create                             api_restream_create
 12271  GET              /api/restream/deck                               api_restream_deck
 11627  GET              /api/restream/health                             api_restream_health
 20860  POST             /api/restream/layout                             api_restream_layout
 19654  GET              /api/restream/list                               api_restream_list
 11596  POST             /api/restream/report                             api_restream_report
 19959  POST             /api/restream/start_all                          api_restream_start_all
 19985  POST             /api/restream/stop_all                           api_restream_stop_all
 11802  GET              /api/restream/testpush                           api_testpush_status
 11827  POST             /api/restream/testpush                           api_testpush_run
 14001  GET              /api/restream/verify                             api_restream_verify
 12759  GET              /api/retention/preview                           api_retention_preview
 12768  POST             /api/retention/run                               api_retention_run
 13385  GET              /api/search                                      api_search
 21602  GET              /api/selftest                                    api_selftest
 19763  GET              /api/shield/stats                                api_shield_stats
 10567  GET              /api/storage                                     api_storage
 10574  POST             /api/storage/cleanup                             api_storage_cleanup
 13522  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11566  GET              /api/stream/timeline                             api_stream_timeline
 12462  GET              /api/stream/transcript                           api_stream_transcript
 10598  GET              /api/summary/preview                             api_summary_preview
 13099  GET              /api/system                                      api_system
 13949  GET              /api/system/check_timing                         api_check_timing
 14064  GET              /api/system/config_drift                         api_config_drift
 12476  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12568  GET              /api/system/preflight                            api_system_preflight
 12694  GET              /api/system/preflight_history                    api_system_preflight_history
 12877  GET              /api/system/resilience                           api_system_resilience
 13420  GET              /api/tags                                        api_tags_list
 10540  GET              /api/top                                         api_top
 10899  GET              /api/trend-7d                                    api_trend_7d
 20122  GET              /api/tts/<fn>                                    api_tts_file
 20882  GET              /api/upload_window                               api_upload_window
 10644  GET              /api/userstats                                   api_userstats
 12194  GET              /api/version                                     api_version
 13072  GET              /archive/<int:eid>/download                      archive_download
 13129  GET              /download/<int:recording_id>                     download
 13012  GET              /health                                          health
 19894  GET              /healthz                                         healthz
 10397  GET              /login                                           dashboard_login_page
 10427  GET              /logout                                          dashboard_logout
 10434  GET              /manifest.webmanifest                            pwa_manifest
 12504  GET              /metrics                                         api_prometheus_metrics
 20821  GET              /overlay                                         overlay_page
 10458  GET              /pwa-icon-<variant>.png                          pwa_icon
 10444  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (254)

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
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
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
 22328  /ai                     
 22787  /ask                    
 22419  /assign_role            
 22465  /ban                    
 23119  /botstats               
 23043  /clearwarns             
 23083  /clip                   
 23068  /clipoftheweek          
 22910  /clips                  
 22380  /create_category        
 22349  /create_channel         
 22408  /create_group           
 22391  /create_role            
 22365  /create_voice           
 22701  /daily                  
 22817  /event                  
 22860  /events                 
 22956  /follow                 
 22940  /help                   
 22454  /kick                   
 22683  /leaderboard            
 22896  /livenow                
 22926  /post_test              
 22757  /profile                
 22489  /purge                  
 22669  /rank                   
 22883  /recstatus              
 22430  /remove_role            
 22342  /restream_status        
 22441  /set_channel_perms      
 22634  /setup_community        
 22652  /setup_targets          
 22982  /stats                  
 22254  /status                 
 23278  /streaminfo             
 23175  /sys_report             
 23151  /sys_unpause            
 22476  /timeout                
 23054  /topstreamers           
 22284  /track                  
 22268  /tracklist              
 22971  /unfollow               
 22317  /untrack                
 23004  /warn                   
 23028  /warnings               
```

## Discord-Events (4)

```
 23764  on_member_join
 23726  on_message
 23365  on_raw_reaction_add
 23799  on_ready
```

## Top-Level-Symbole in bot.py (491 Funktionen, 2 Klassen)

```
  2512-2513   _abo_key
  2533-2551   _abo_probe_dump
 21124-21134  _active_recorder_sync
 16926-16933  _ad_allowlist
 18064-18070  _agent_for
 21136-21154  _ai_calls_total_sync
 18073-18089  _ai_telemetry
 18577-18595  _alert
 23915-23965  _alert_monitor_loop
 24346-24408  _announce_loop
  3454-3457   _anthropic_key
  3464-3466   _anthropic_model
 10150-10153  _arg_int
  2504-2509   _as_dict
 18731-18753  _audio_tap_cmd
 10318-10329  _auth_cookie
 10285-10314  _auth_guard
  1660-1665   _auto_on
 19630-19648  _auto_restream_loop
 25464-25479  _azrael_broadcast_reply
 25364-25386  _azrael_chat_reply
 25347-25361  _azrael_chat_should_reply
 25392-25394  _azrael_gate_cfg
 18094-18108  _azrael_live_state
 20733-20747  _azrael_overlay_state
 18460-18514  _azrael_proactive_loop
 17912-17968  _azrael_reaction_to_chats
 25397-25404  _azrael_reply_all_chats
 25334-25344  _azrael_self_names
 25432-25461  _azrael_send_to
 18114-18135  _azrael_system
 24084-24087  _backup_active
 24165-24178  _backup_loop
 23877-23886  _brain_growth_loop
 10950-10977  _brain_growth_snapshot
  2440-2460   _brain_hint_delay
  6545-6573   _brain_notify
 12791-12808  _browser_push
  6589-6676   _build_daily_summary
  2943-3123   _build_native_cmd
 15114-15301  _build_restream_cmd
  3167-3200   _build_ytdlp_cmd
 21076-21083  _cached_probe
  5367-5394   _can_stop_tracking
  1840-1862   _capture_set_cookies
 13685-13688  _cfg_get
 13691-13693  _cfg_set
 20507-20542  _channel_set_all
 14348-14351  _chat_connected
 14354-14370  _chat_disconnected
  8641-8652   _chat_is_forum
 14390-14392  _chat_sanitize
 14394-14403  _chat_src_ok
 14333-14345  _chat_stat
 14373-14376  _chat_stats_snapshot
  3729-3740   _check_ai_alive_sync
  3743-3755   _check_ai_models_sync
 21085-21098  _check_redis_alive_sync
 21100-21120  _check_redis_version_sync
 11245-11288  _classify_pool_anonymity
 11291-11308  _classify_pool_anonymity_bg
   818-822    _claude_chat_sync_metered
 10179-10186  _client_ip
 24440-24467  _clip_prune
 24470-24480  _clip_recfile_for
 24993-24999  _clip_should_velocity
 24521-24603  _clip_to_discord
  3627-3636   _close_ai_session
 25510-25525  _cohost_broadcast
 25495-25496  _cohost_cfg
 25551-25563  _cohost_fire_highlight
 25499-25507  _cohost_gate
 25528-25548  _cohost_highlight
 24652-24686  _community_events_loop
 10798-10800  _conv_messages
  6953-6996   _cookie_alarm_loop
  1912-1916   _cookie_autorefresh_info
  1817-1821   _cookie_header
 12841-12873  _cpu_load_snapshot
  3949-3961   _create_index_safe
 21357-21463  _crowdsec_status
 21303-21354  _crowdsec_via_lapi
 21168-21186  _cscli_bin
 21192-21205  _cscli_path
  6843-6868   _daily_summary_loop
 21223-21240  _darf_journal_lesen
 23889-23912  _db_maintenance_loop
  6812-6840   _db_vacuum_loop
 16949-16973  _detect_foreign_ad
  1398-1409   _diag_path_owner
 18366-18410  _director_finalize
 19177-19184  _director_for
 18315-18363  _director_mark
 24887-24922  _disc_automod_check
 24863-24866  _disc_state_get
 24869-24876  _disc_state_set
 21906-21919  _discord_guild_filesize_bytes
 22111-22115  _discord_invite
 24824-24860  _discord_live_thread
 18517-18529  _discord_notify
 22010-22035  _discord_ops_alert
 24722-24820  _discord_post_user
 22171-23874  _discord_run_once
 22050-22108  _discord_start
 24411-24417  _discord_stop
 21927-21929  _discord_upload_limit_label
 21922-21924  _discord_upload_limit_mb
  6871-6948   _disk_alarm_loop
 26947-26996  _disk_autoclean
 26999-27012  _disk_guard_loop
 26939-26944  _disk_pct
 14707-14709  _drawtext_chain
 13228-13230  _dump_all_threads
 11170-11234  _enrich_proxies_with_geo
  2057-2101   _ensure_cookie_file_netscape
 22118-22168  _ensure_discord_invite
 24617-24649  _ensure_error_channel
  8700-8703   _ensure_notify_topic
 11415-11452  _ensure_proxy_ready
  8654-8681   _ensure_topic
   675-677    _env_int
   680-682    _env_int_range
 24689-24719  _error_channel_loop
 18561-18574  _event_webhook
 14151-14164  _evolution_loop
  5987-6021   _extract_file_payload
  2189-2191   _extract_urls_from_streamurl_node
 21208-21215  _f2b_sudo_hint
 18597-18599  _faster_whisper_available
 11059-11077  _fetch_proxy_list
 19011-19039  _fetch_tiktok_room_id
   751-754    _ff_cmd
 14873-14878  _find_chromium
  3160-3164   _find_external_recorder
  2194-2196   _find_stream_urls
 13736-13761  _fire_webhooks
  7732-7741   _fork_safe
   833-842    _freeai_chat_sync_metered
 21258-21300  _geo_lookup_ips
  3616-3625   _get_ai_session
  7566-7606   _get_live_info
  2730-2737   _get_resolve_semaphore
  7996-8362   _handle_single_tracking
 26765-26767  _hb
 26770-26787  _hb_while
 14408-14410  _highlight_cfg
 14413-14442  _highlight_observe
 14881-14899  _htmlov_screenshot_cmd
 18755-18765  _httpx_proxy
 13769-13781  _in_quiet_hours
 27838-27869  _install_fast_eventloop
 10045-10099  _install_fast_json
 13233-13249  _install_faulthandler
 19802-19811  _intel_ensure_schema
 19849-19884  _intel_index_loop
 19823-19833  _intel_index_one
 19814-19820  _intel_semantic
  5356-5365   _is_authorized
  7897-7903   _is_dead
  2179-2181   _is_hevc
 21243-21249  _is_private_ip
  1562-1569   _is_process_running
  6575-6586   _is_quiet_hours
  1199-1208   _is_upload_window
 10134-10147  _json_error_handler
  6798-6799   _kick_broadcaster_id
 11728-11747  _kick_channel_live
  6710-6752   _kick_follower_count
  6694-6697   _kick_slug
 12221-12252  _kick_user_token
  3998-4001   _kind_from_filename
 13798-13803  _latest_popularity
 19392-19425  _live_react_loop
 19188-19381  _live_react_worker
 17971-17982  _live_transcript_push
 19383-19390  _live_users
 18413-18457  _living_title_loop
  1738-1811   _load_cookies_dict
 24090-24162  _local_backup_scan
 10116-10130  _log_5xx
 15309-15321  _looks_like_codec_err
 15304-15306  _looks_like_source_expired
  7813-7843   _loop_fehler
 13253-13262  _loop_heartbeat
 26735-26762  _loop_lag_monitor
 13265-13333  _loop_watchdog_thread
 17851-17865  _loyalty_add
 17842-17848  _loyalty_get
 17868-17876  _loyalty_top
 13935-13937  _manual_donations_total
  7905-7906   _mark_dead
 11899-11915  _marketing_loop
 25411-25429  _maybe_handle_command
 27098-27122  _maybe_hype_clip
  3916-3939   _migrate_columns
 25690-25701  _mod_is_exempt
 25704-25709  _mod_warn_first
 25712-25715  _mod_warn_text
 14191-14199  _modlog
   952-954    _multistream_targets
  7744-7745   _nc_create_subprocess_exec
  7748-7749   _nc_create_subprocess_shell
 12151-12168  _news_loop
 14229-14231  _normalize_ingest
  2371-2388   _note_check_duration
  8694-8697   _notify_topic_name
 17997-18005  _oracle_memories
 18270-18304  _oracle_memorize
 18008-18021  _oracle_persona
 17990-17994  _oracle_recent_text
 14533-14541  _ov_atomic_write
 14521-14527  _ov_bar
 16852-16864  _ov_clip_text
 14530-14531  _ov_oneline
 20785-20814  _overlay_push
 14827-14870  _overlay_render_size
 14295-14299  _overlay_session_reset
 20749-20752  _overlay_src_ok
 16936-16946  _own_invites
 14822-14824  _parse_size
 21471-21551  _parse_ssh_attacks
  7168-7201   _pause_resume_cmd
  1866-1910   _persist_refreshed_cookies
  1704-1736   _pick_checked_pull_proxy
 10215-10228  _pin_auth_value
 10274-10275  _pin_clear_fail
 10254-10257  _pin_locked
 10260-10271  _pin_note_fail
 10231-10251  _pin_ok
 20643-20668  _piper_pick_model
 20680-20727  _piper_say
 13698-13733  _post_json_threaded
 14801-14819  _probe_video_size
  1590-1607   _proc_is_recorder
 11157-11168  _proxy_geo_cache_put
 11384-11412  _proxy_pool_refresh_loop
  1670-1701   _proxy_report_recording
 13218-13220  _prune_stall_dumps
 11969-12090  _public_stats
 18532-18558  _push_notify
 10376-10378  _pwa_dir
 11128-11143  _quick_validate_proxy
 13764-13766  _quiet_hours_config
 10341-10374  _rate_guard
 17816-17822  _react_warn
  7652-7691   _reap_proc
  2411-2433   _record_check_outcome
   746-748    _redact_stream_urls
 11311-11381  _refresh_proxy_pool
  2205-2295   _resolve_via_html
  2553-2707   _resolve_via_webcast_api_v2
  2770-2832   _resolve_via_ytdlp
 25038-25167  _resolve_youtube_ingest
 19464-19471  _restream_active_platforms
 14278-14289  _restream_active_sources
 19042-19141  _restream_chat_guardian
 14445-14517  _restream_chat_push
 14202-14214  _restream_enabled
 14902-14989  _restream_html_overlay_start
 14992-15005  _restream_html_overlay_stop
  1147-1149   _restream_layout_mode
 14240-14263  _restream_overlay_files
 19429-19461  _restream_platform_state
 19592-19627  _restream_resume_after_restart
 15053-15111  _restream_tts_enqueue_wav
 14763-14795  _restream_tts_feeder
 14760-14761  _restream_tts_fifo_path
 15008-15035  _restream_tts_start
 15037-15051  _restream_tts_stop
 19474-19589  _restream_verify_loop
 24055-24067  _retention_loop
 24014-24052  _retention_scan
  2515-2517   _room_is_abo
  6025-6142   _run_ai_call
 13356-13369  _run_async_from_flask
 21252-21255  _run_priv
 27826-27834  _run_selfcheck_and_exit
 24070-24081  _s3_client
  7932-7983   _safe_send
  4620-4636   _sample_net_throughput
  2463-2490   _schedule_next_check
 23968-24011  _scheduler_loop
  3942-3946   _schema_pk
 13373-13378  _scraper_session
 25718-25757  _screen_full
 12417-12454  _sec_headers
  2184-2186   _select_stream_from_data_section
 27639-27823  _selfcheck
  8706-8740   _send_live_notice
  1222-1226   _should_defer_upload
 24483-24518  _shrink_for_discord
 10381-10393  _sicheres_ziel
 27019-27036  _sign_health_check
 27039-27058  _sign_health_loop
  7761-7772   _spawn
  7775-7805   _spawn_from_flask
 21595-21598  _st_befund
 18767-19008  _start_chat_listener
 13336-13353  _start_loop_watchdog
 12114-12142  _stats_loop
 12093-12096  _stats_output_path
 12099-12111  _stats_write
  8434-8450   _storage_cleanup_loop
 27078-27085  _story_for
  3222-3228   _stream_url_expiry
  3237-3243   _stream_url_is_fresh
  3230-3235   _stream_url_ttl
 16899-16906  _streamer_persona_get
 14712-14716  _studio_chain
 24187-24309  _system_backup
 24312-24342  _system_backup_loop
 11080-11119  _test_proxy
 11769-11778  _testpush_cfg
 11781-11798  _testpush_exec
 11750-11766  _testpush_resolve_live
  7908-7929   _tg_sprache_setzen
  8613-8623   _tg_topics_load_into_mem
  8610-8611   _tg_topics_path
  8625-8632   _tg_topics_save
 10189-10197  _token_ok
  8635-8639   _topic_forget
 13784-13795  _tracking_max_duration
  4207-4221   _tracking_remove_cleanup
  4238-4250   _tracking_resume_cleanup
  1456-1479   _try_attach_file_handler
 20670-20678  _tts_cleanup
 11706-11710  _tunnel_effective
 20166-20219  _twitch_channel_status
 25760-25905  _twitch_chat_loop
 25574-25677  _twitch_eventsub_loop
  1245-1258   _upload_queue_add
  1269-1271   _upload_queue_count
  1228-1237   _upload_queue_load
  1218-1220   _upload_queue_path
  1260-1267   _upload_queue_remove
  1239-1243   _upload_queue_save
  1273-1314   _upload_window_loop
  7625-7632   _uptime_s
 14217-14226  _url_host
   726-743    _url_ohne_zugang
   811-815    _usage_record_claude
  7846-7890   _verbindung_verloren
  6755-6786   _viewer_sample_loop
  6802-6809   _viewer_stats
 10278-10281  _wants_html
  7635-7649   _warn_empty_env
 26808-26929  _watchdog_loop
 25313-25321  _wchat_thank_ok
 18601-18631  _whisper_get_model
  7722-7729   _whisper_native_section
 17803-17809  _whisper_pool
 18700-18729  _whisper_segments
 18633-18697  _whisper_transcribe
 14543-14705  _write_restream_overlay
 25933-26013  _youtube_api_chat_loop
 20222-20325  _youtube_api_status
 20328-20395  _youtube_channel_status
 26016-26177  _youtube_chat_loop
 25173-25186  _youtube_restream_autoconfig
 25189-25213  _youtube_restream_autoconfig_inner
 25280-25308  _youtube_send
 20463-20504  _youtube_set_channel
 25216-25250  _yt_access_token
 25253-25268  _yt_live_chat_id
 25926-25930  _yt_oauth_configured
 25276-25277  _yt_sendrate_cfg
 25908-25923  _yt_timeout
  2754-2755   _ytdlp_detect_available
  2757-2768   _ytdlp_note_result
 13223-13225  _zombie_child_count
  7502-7526   about
  4117-4121   add_ai_log_entry
  4034-4037   add_archive_entry
  4733-4748   add_archive_rule
  4409-4443   add_recording
  4182-4199   add_tracking
  6145-6178   ai
  3769-3820   ai_chat
  3854-3864   ai_history_append
  3866-3871   ai_history_clear
  3843-3852   ai_history_load
  3828-3841   ai_rate_limit_check
  6207-6215   aireset
 18138-18157  azrael_chat
 26182-26304  brain_cmd
  3246-3430   build_recording_cmd
  4202-4205   bulk_add_trackings
  6999-7058   bulkadd
  8453-8593   check_all_trackings
  4254-4266   claim_live_transition
 16976-17738  class KickModerator
 15324-16739  class RestreamManager
 11498-11540  classify_proxy_anonymity
  6253-6451   cleanup
  5216-5257   cleanup_old_recordings
  4400-4407   clear_recording
 24925-24990  clip_moment
  4564-4613   compute_storage_forecast
  7121-7165   cookies_cmd
  4173-4179   count_trackings_for_chat
  4104-4115   decide_preferred_recorder
  4044-4047   delete_archive_entry
  4750-4758   delete_archive_rule
  5682-5829   diag
 26416-26477  einnahmen_cmd
  4558-4561   find_recordings_by_fingerprint
  4065-4081   finish_recording_attempt
  4226-4228   get_all_active_trackings
  4132-4135   get_all_checks
  4445-4448   get_all_recordings
  4507-4509   get_all_tags_with_counts
  4535-4538   get_annotations_for_recording
  4039-4042   get_archive_entry
  4528-4531   get_bookmarked_recordings
  1933-2050   get_cookie_health
  4495-4501   get_event_log
  4088-4102   get_last_recording_attempt
  2835-2940   get_live_status
  5016-5019   get_manual_recordings
  4543-4546   get_or_compute_inspect_sync
  5292-5336   get_outcome_breakdown
  4514-4517   get_priority_poll_interval
  4711-4720   get_profile_snapshots
  4083-4086   get_recent_recording_attempts
  4450-4453   get_recording_by_id
  4521-4524   get_recording_note
  3564-3587   get_redis
  4162-4165   get_stats
  5183-5214   get_storage_stats
  4851-4853   get_tiktok_status_distribution
  4268-4277   get_tracking_state
  4223-4224   get_trackings_for_group
  5032-5035   get_trash_recordings
  9361-10024  handle_recording_finished
  3964-3989   init_db
  5106-5160   inspect_stream_url
  4723-4731   list_archive_rules
  5486-5524   live
  7986-7994   live_check_worker
  3639-3673   llm_chat
  3696-3724   llm_chat_sync
  3681-3693   llm_list_models
  4461-4487   log_event
  1524-1557   log_recording_failure
  7315-7364   logs_cmd
 27126-27629  main
  6181-6204   on_ai_media
  7441-7467   on_ai_reply
  7470-7499   on_azrael_mention
  7531-7561   on_callback
 18163-18267  oracle_handle
  7204-7207   pause_tracking
  5346-5351   profile_keyboard
  7266-7312   quota
  8364-8431   reaper_loop
  4847-4849   record_tiktok_status
  6220-6250   recstatus
  3589-3597   redis_get_json
  3599-3605   redis_set_json
 26480-26490  report_cmd
 11543-11545  report_proxy_result
  2298-2325   resolve_tiktok_live_stream
  5027-5030   restore_recording
  7210-7213   resume_tracking
  4761-4841   run_archive_rules
 26493-26715  run_bot
 13143-13190  run_flask
  4639-4684   sample_bandwidth_for_active
  4690-4709   save_profile_snapshot
  4124-4130   save_tiktok_check
  4392-4398   set_recording_file
  4231-4235   set_tracking_paused
  5022-5025   soft_delete_recording
  8746-9359   split_and_send_video
  5399-5441   start
  4049-4063   start_recording_attempt
  6454-6492   stats
  4997-5014   stop_manual_recording
  7216-7263   stoprec
  6679-6687   summary_cmd
  7367-7438   sysres
  5831-5975   teststream
  5443-5484   tiktok
  7061-7118   topusers
  5561-5618   track
  5526-5558   track_exact
  5632-5680   tracklist
  4863-4995   trigger_manual_recording
  4353-4390   try_acquire_recording_lock
  5038-5097   universal_search
  5620-5630   untrack
 26307-26413  update_cmd
  4553-4556   update_recording_fingerprint
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
brainstate.py          history_for, record, stall, stream_recent
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
