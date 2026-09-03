# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (134)

```
 10474  GET              /                                                dashboard
 13939  GET              /api/abo/status                                  api_abo_status
 10547  GET              /api/active-recordings                           api_active_recordings
 14010  GET              /api/activity-pulse                              api_activity_pulse
 13817  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20433  GET/POST         /api/audio/config                                api_audio_config
 20463  POST             /api/audio/testtone                              api_audio_testtone
 13883  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13907  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13911  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12001  GET              /api/automation/status                           api_automation_status
 12023  POST             /api/automation/toggle                           api_automation_toggle
 12945  GET              /api/azrael/agents                               api_azrael_agents
 11893  POST             /api/azrael/ask                                  api_azrael_ask
 20522  GET/POST         /api/azrael/context                              api_azrael_context
 12743  GET              /api/azrael/core                                 api_azrael_core
 20673  POST             /api/azrael/live_pause                           api_azrael_live_pause
 20663  GET              /api/azrael/live_status                          api_azrael_live_status
 20681  POST             /api/azrael/live_test                            api_azrael_live_test
 12954  GET              /api/azrael/memories                             api_azrael_memories
 20729  POST             /api/azrael/persona                              api_azrael_persona_set
 20720  GET              /api/azrael/personas                             api_azrael_personas
 20757  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20495  POST             /api/azrael/react                                api_azrael_react
 20531  GET              /api/azrael/reaction                             api_azrael_reaction
 20700  GET              /api/azrael/reactions                            api_azrael_reactions
 20750  GET              /api/azrael/transcript                           api_azrael_transcript
 20635  POST             /api/azrael/tts_test                             api_azrael_tts_test
 20606  GET              /api/azrael/voices                               api_azrael_voices
 20774  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10846  GET              /api/backoff-watch                               api_backoff_watch
 13379  POST             /api/backup/run                                  api_backup_run
 13345  GET              /api/backup/status                               api_backup_status
 13334  POST             /api/backup/system                               api_backup_system
 13849  GET              /api/bandwidth/live                              api_bandwidth_live
 13802  GET              /api/bookmarks                                   api_bookmarks_list
 11109  GET              /api/brain                                       api_brain
 11046  GET              /api/brain/alarms                                api_brain_alarms
 11031  GET              /api/brain/creator                               api_brain_creator
 11008  GET              /api/brain/graph                                 api_brain_graph
 11069  GET              /api/brain/growth                                api_brain_growth
 10024  GET              /api/brain/health                                api_brain_health
 21182  GET              /api/channel/categories                          api_channel_categories
 21188  POST             /api/channel/set                                 api_channel_set
 21035  GET              /api/channels/status                             api_channels_status
 10528  GET              /api/checks                                      api_checks
 20559  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20542  GET              /api/clips                                       api_clips
 20588  POST/DELETE      /api/clips/clear                                 api_clips_clear
 14318  GET              /api/community/stats                             api_community_stats
 21822  GET              /api/data/export                                 api_data_export
 20326  GET              /api/debug/threads                               api_debug_threads
 22669  GET              /api/defense/attacks                             api_defense_attacks
 22636  GET              /api/defense/crowdsec                            api_defense_crowdsec
 22654  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22360  GET              /api/defense/overview                            api_defense_overview
 13831  GET              /api/events                                      api_events
 13216  GET              /api/events/stream                               api_events_stream
 13844  GET              /api/forecast/storage                            api_forecast_storage
 12039  GET              /api/freeai/status                               api_freeai_status
 12786  GET              /api/health                                      api_health
 13862  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13858  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20404  GET              /api/highlights                                  api_highlights
 20416  POST             /api/highlights/config                           api_highlights_config
 10408  POST             /api/login                                       dashboard_login_submit
 14303  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14272  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13114  GET              /api/notify/status                               api_notify_status
 13125  POST             /api/notify/test                                 api_notify_test
 10632  GET              /api/outcomes                                    api_outcomes
 21659  POST             /api/overlay/config                              api_overlay_config
 21646  POST             /api/overlay/event                               api_overlay_event
 21551  GET              /api/overlay/state                               api_overlay_state
 10665  GET              /api/profile/<username>                          api_profile
 14028  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13870  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13993  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13970  GET              /api/proxy/trend                                 api_proxy_trend
 12494  GET              /api/public/stats                                api_public_stats
 10508  GET              /api/pulse                                       api_pulse
 13438  GET              /api/recording-attempts                          api_recording_attempts
 20128  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20106  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20147  POST             /api/restream/<int:rid>/start                    api_restream_start
 20347  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21513  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20082  POST             /api/restream/create                             api_restream_create
 12619  GET              /api/restream/deck                               api_restream_deck
 11975  GET              /api/restream/health                             api_restream_health
 21535  POST             /api/restream/layout                             api_restream_layout
 20055  GET              /api/restream/list                               api_restream_list
 11944  POST             /api/restream/report                             api_restream_report
 20360  POST             /api/restream/start_all                          api_restream_start_all
 20386  POST             /api/restream/stop_all                           api_restream_stop_all
 12150  GET              /api/restream/testpush                           api_testpush_status
 12175  POST             /api/restream/testpush                           api_testpush_run
 14403  GET              /api/restream/verify                             api_restream_verify
 13163  GET              /api/retention/preview                           api_retention_preview
 13172  POST             /api/retention/run                               api_retention_run
 13787  GET              /api/search                                      api_search
 22407  GET              /api/selftest                                    api_selftest
 20164  GET              /api/shield/stats                                api_shield_stats
 10569  GET              /api/storage                                     api_storage
 10576  POST             /api/storage/cleanup                             api_storage_cleanup
 13924  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11914  GET              /api/stream/timeline                             api_stream_timeline
 12847  GET              /api/stream/transcript                           api_stream_transcript
 10600  GET              /api/summary/preview                             api_summary_preview
 13503  GET              /api/system                                      api_system
 14351  GET              /api/system/check_timing                         api_check_timing
 14466  GET              /api/system/config_drift                         api_config_drift
 12861  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12972  GET              /api/system/preflight                            api_system_preflight
 13098  GET              /api/system/preflight_history                    api_system_preflight_history
 13281  GET              /api/system/resilience                           api_system_resilience
 13822  GET              /api/tags                                        api_tags_list
 10542  GET              /api/top                                         api_top
 10901  GET              /api/trend-7d                                    api_trend_7d
 20620  GET              /api/tts/<fn>                                    api_tts_file
 21687  GET              /api/upload_window                               api_upload_window
 10646  GET              /api/userstats                                   api_userstats
 12542  GET              /api/version                                     api_version
 13476  GET              /archive/<int:eid>/download                      archive_download
 13533  GET              /download/<int:recording_id>                     download
 13416  GET              /health                                          health
 20295  GET              /healthz                                         healthz
 10399  GET              /login                                           dashboard_login_page
 10429  GET              /logout                                          dashboard_logout
 10436  GET              /manifest.webmanifest                            pwa_manifest
 12889  GET              /metrics                                         api_prometheus_metrics
 21496  GET              /overlay                                         overlay_page
 10460  GET              /pwa-icon-<variant>.png                          pwa_icon
 10446  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (225)

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
    65  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    37  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
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
   227  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   153  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   171  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   143  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    46  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   119  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
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
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   103  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   151  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   168  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   199  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   175  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   205  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    66  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   219  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
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
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
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
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 23133  /ai                     
 23592  /ask                    
 23224  /assign_role            
 23270  /ban                    
 23924  /botstats               
 23848  /clearwarns             
 23888  /clip                   
 23873  /clipoftheweek          
 23715  /clips                  
 23185  /create_category        
 23154  /create_channel         
 23213  /create_group           
 23196  /create_role            
 23170  /create_voice           
 23506  /daily                  
 23622  /event                  
 23665  /events                 
 23761  /follow                 
 23745  /help                   
 23259  /kick                   
 23488  /leaderboard            
 23701  /livenow                
 23731  /post_test              
 23562  /profile                
 23294  /purge                  
 23474  /rank                   
 23688  /recstatus              
 23235  /remove_role            
 23147  /restream_status        
 23246  /set_channel_perms      
 23439  /setup_community        
 23457  /setup_targets          
 23787  /stats                  
 23059  /status                 
 24083  /streaminfo             
 23980  /sys_report             
 23956  /sys_unpause            
 23281  /timeout                
 23859  /topstreamers           
 23089  /track                  
 23073  /tracklist              
 23776  /unfollow               
 23122  /untrack                
 23809  /warn                   
 23833  /warnings               
```

## Discord-Events (4)

```
 24569  on_member_join
 24531  on_message
 24170  on_raw_reaction_add
 24604  on_ready
```

## Top-Level-Symbole in bot.py (503 Funktionen, 2 Klassen)

```
  2503-2504   _abo_key
  2524-2542   _abo_probe_dump
 21929-21939  _active_recorder_sync
 17337-17344  _ad_allowlist
 18471-18477  _agent_for
 21941-21959  _ai_calls_total_sync
 18480-18496  _ai_telemetry
 18978-18996  _alert
 24720-24770  _alert_monitor_loop
 25151-25213  _announce_loop
  3445-3448   _anthropic_key
  3455-3457   _anthropic_model
 10152-10155  _arg_int
  2495-2500   _as_dict
 15150-15155  _audio_cfg
 19132-19154  _audio_tap_cmd
 10320-10331  _auth_cookie
 10287-10316  _auth_guard
  1651-1656   _auto_on
 20031-20049  _auto_restream_loop
 26269-26284  _azrael_broadcast_reply
 26169-26191  _azrael_chat_reply
 26152-26166  _azrael_chat_should_reply
 26197-26199  _azrael_gate_cfg
 18501-18515  _azrael_live_state
 21399-21413  _azrael_overlay_state
 18861-18915  _azrael_proactive_loop
 18320-18376  _azrael_reaction_to_chats
 26202-26209  _azrael_reply_all_chats
 26139-26149  _azrael_self_names
 26237-26266  _azrael_send_to
 18518-18539  _azrael_system
 24889-24892  _backup_active
 24970-24983  _backup_loop
 24682-24691  _brain_growth_loop
 10977-11004  _brain_growth_snapshot
  2431-2451   _brain_hint_delay
 10969-10971  _brain_history_for
  6536-6564   _brain_notify
 10946-10967  _brain_record
 10973-10975  _brain_stream_recent
 13195-13212  _browser_push
  6580-6667   _build_daily_summary
  2934-3114   _build_native_cmd
 15511-15698  _build_restream_cmd
  3158-3191   _build_ytdlp_cmd
 21881-21888  _cached_probe
  5358-5385   _can_stop_tracking
  1831-1853   _capture_set_cookies
 14087-14090  _cfg_get
 14093-14095  _cfg_set
 21143-21178  _channel_set_all
 14748-14751  _chat_connected
 14754-14770  _chat_disconnected
  8632-8643   _chat_is_forum
 14790-14792  _chat_sanitize
 14794-14803  _chat_src_ok
 14733-14745  _chat_stat
 14773-14776  _chat_stats_snapshot
  3720-3731   _check_ai_alive_sync
  3734-3746   _check_ai_models_sync
 21890-21903  _check_redis_alive_sync
 21905-21925  _check_redis_version_sync
 11576-11619  _classify_pool_anonymity
 11622-11639  _classify_pool_anonymity_bg
   809-813    _claude_chat_sync_metered
 10181-10188  _client_ip
 25245-25272  _clip_prune
 25275-25285  _clip_recfile_for
 25798-25804  _clip_should_velocity
 25326-25408  _clip_to_discord
  3618-3627   _close_ai_session
 26315-26330  _cohost_broadcast
 26300-26301  _cohost_cfg
 26356-26368  _cohost_fire_highlight
 26304-26312  _cohost_gate
 26333-26353  _cohost_highlight
 25457-25491  _community_events_loop
 10800-10802  _conv_messages
  6944-6987   _cookie_alarm_loop
  1903-1907   _cookie_autorefresh_info
  1808-1812   _cookie_header
 13245-13277  _cpu_load_snapshot
  3940-3952   _create_index_safe
 22162-22268  _crowdsec_status
 22108-22159  _crowdsec_via_lapi
 21973-21991  _cscli_bin
 21997-22010  _cscli_path
  6834-6859   _daily_summary_loop
 22028-22045  _darf_journal_lesen
 24694-24717  _db_maintenance_loop
  6803-6831   _db_vacuum_loop
 17360-17384  _detect_foreign_ad
  1389-1400   _diag_path_owner
 18767-18811  _director_finalize
 19578-19585  _director_for
 18716-18764  _director_mark
 25692-25727  _disc_automod_check
 25668-25671  _disc_state_get
 25674-25681  _disc_state_set
 22711-22724  _discord_guild_filesize_bytes
 22916-22920  _discord_invite
 25629-25665  _discord_live_thread
 18918-18930  _discord_notify
 22815-22840  _discord_ops_alert
 25527-25625  _discord_post_user
 22976-24679  _discord_run_once
 22855-22913  _discord_start
 25216-25222  _discord_stop
 22732-22734  _discord_upload_limit_label
 22727-22729  _discord_upload_limit_mb
  6862-6939   _disk_alarm_loop
 27752-27801  _disk_autoclean
 27804-27817  _disk_guard_loop
 27744-27749  _disk_pct
 15107-15109  _drawtext_chain
 13630-13632  _dump_all_threads
 11501-11565  _enrich_proxies_with_geo
  2048-2092   _ensure_cookie_file_netscape
 22923-22973  _ensure_discord_invite
 25422-25454  _ensure_error_channel
  8691-8694   _ensure_notify_topic
 11746-11783  _ensure_proxy_ready
  8645-8672   _ensure_topic
   666-668    _env_int
   671-673    _env_int_range
 25494-25524  _error_channel_loop
 18962-18975  _event_webhook
 14553-14566  _evolution_loop
  5978-6012   _extract_file_payload
  2180-2182   _extract_urls_from_streamurl_node
 22013-22020  _f2b_sudo_hint
 18998-19000  _faster_whisper_available
 11390-11408  _fetch_proxy_list
 19412-19440  _fetch_tiktok_room_id
   742-745    _ff_cmd
 15270-15275  _find_chromium
  3151-3155   _find_external_recorder
  2185-2187   _find_stream_urls
 14138-14163  _fire_webhooks
  7723-7732   _fork_safe
   824-833    _freeai_chat_sync_metered
 22063-22105  _geo_lookup_ips
  3607-3616   _get_ai_session
  7557-7597   _get_live_info
  2721-2728   _get_resolve_semaphore
  7987-8353   _handle_single_tracking
 27570-27572  _hb
 27575-27592  _hb_while
 14808-14810  _highlight_cfg
 14813-14842  _highlight_observe
 15278-15296  _htmlov_screenshot_cmd
 19156-19166  _httpx_proxy
 14171-14183  _in_quiet_hours
 28643-28674  _install_fast_eventloop
 10047-10101  _install_fast_json
 13635-13651  _install_faulthandler
 20203-20212  _intel_ensure_schema
 20250-20285  _intel_index_loop
 20224-20234  _intel_index_one
 20215-20221  _intel_semantic
  5347-5356   _is_authorized
  7888-7894   _is_dead
  2170-2172   _is_hevc
 22048-22054  _is_private_ip
  1553-1560   _is_process_running
  6566-6577   _is_quiet_hours
  1190-1199   _is_upload_window
 10136-10149  _json_error_handler
  6789-6790   _kick_broadcaster_id
 12076-12095  _kick_channel_live
  6701-6743   _kick_follower_count
  6685-6688   _kick_slug
 12569-12600  _kick_user_token
  3989-3992   _kind_from_filename
 14200-14205  _latest_popularity
 19793-19826  _live_react_loop
 19589-19782  _live_react_worker
 18379-18390  _live_transcript_push
 19784-19791  _live_users
 18814-18858  _living_title_loop
  1729-1802   _load_cookies_dict
 24895-24967  _local_backup_scan
 10118-10132  _log_5xx
 15706-15718  _looks_like_codec_err
 15701-15703  _looks_like_source_expired
  7804-7834   _loop_fehler
 13655-13664  _loop_heartbeat
 27540-27567  _loop_lag_monitor
 13667-13735  _loop_watchdog_thread
 18259-18273  _loyalty_add
 18250-18256  _loyalty_get
 18276-18284  _loyalty_top
 14337-14339  _manual_donations_total
  7896-7897   _mark_dead
 12247-12263  _marketing_loop
 26216-26234  _maybe_handle_command
 27903-27927  _maybe_hype_clip
  3907-3930   _migrate_columns
 26495-26506  _mod_is_exempt
 26509-26514  _mod_warn_first
 26517-26520  _mod_warn_text
 14593-14601  _modlog
   943-945    _multistream_targets
  7735-7736   _nc_create_subprocess_exec
  7739-7740   _nc_create_subprocess_shell
 12499-12516  _news_loop
 14631-14633  _normalize_ingest
  2362-2379   _note_check_duration
  8685-8688   _notify_topic_name
 18405-18413  _oracle_memories
 18671-18705  _oracle_memorize
 18416-18429  _oracle_persona
 18398-18402  _oracle_recent_text
 14933-14941  _ov_atomic_write
 14921-14927  _ov_bar
 17249-17261  _ov_clip_text
 14930-14931  _ov_oneline
 21463-21492  _overlay_push
 15224-15267  _overlay_render_size
 14695-14699  _overlay_session_reset
 21415-21418  _overlay_src_ok
 17347-17357  _own_invites
 15219-15221  _parse_size
 22276-22356  _parse_ssh_attacks
  7159-7192   _pause_resume_cmd
  1857-1901   _persist_refreshed_cookies
  1695-1727   _pick_checked_pull_proxy
 10217-10230  _pin_auth_value
 10276-10277  _pin_clear_fail
 10256-10259  _pin_locked
 10262-10273  _pin_note_fail
 10233-10253  _pin_ok
 21305-21307  _piper_available
 21270-21292  _piper_list_voices
 21312-21337  _piper_pick_model
 21349-21396  _piper_say
 21263-21267  _piper_voice_roots
 14100-14135  _post_json_threaded
 15198-15216  _probe_video_size
  1581-1598   _proc_is_recorder
 11488-11499  _proxy_geo_cache_put
 11715-11743  _proxy_pool_refresh_loop
  1661-1692   _proxy_report_recording
 13620-13622  _prune_stall_dumps
 12317-12438  _public_stats
 18933-18959  _push_notify
 10378-10380  _pwa_dir
 11459-11474  _quick_validate_proxy
 14166-14168  _quiet_hours_config
 10343-10376  _rate_guard
 18224-18230  _react_warn
  7643-7682   _reap_proc
  2402-2424   _record_check_outcome
   737-739    _redact_stream_urls
 11642-11712  _refresh_proxy_pool
 21295-21301  _resolve_piper_model
  2196-2286   _resolve_via_html
  2544-2698   _resolve_via_webcast_api_v2
  2761-2823   _resolve_via_ytdlp
 25843-25972  _resolve_youtube_ingest
 19865-19872  _restream_active_platforms
 14680-14691  _restream_active_sources
 19443-19542  _restream_chat_guardian
 14845-14917  _restream_chat_push
 14604-14616  _restream_enabled
 15299-15386  _restream_html_overlay_start
 15389-15402  _restream_html_overlay_stop
  1138-1140   _restream_layout_mode
 14642-14665  _restream_overlay_files
 19830-19862  _restream_platform_state
 19993-20028  _restream_resume_after_restart
 15450-15508  _restream_tts_enqueue_wav
 15160-15192  _restream_tts_feeder
 15157-15158  _restream_tts_fifo_path
 15405-15432  _restream_tts_start
 15434-15448  _restream_tts_stop
 19875-19990  _restream_verify_loop
 24860-24872  _retention_loop
 24819-24857  _retention_scan
  2506-2508   _room_is_abo
  6016-6133   _run_ai_call
 13758-13771  _run_async_from_flask
 22057-22060  _run_priv
 28631-28639  _run_selfcheck_and_exit
 24875-24886  _s3_client
  7923-7974   _safe_send
  4611-4627   _sample_net_throughput
  2454-2481   _schedule_next_check
 24773-24816  _scheduler_loop
  3933-3937   _schema_pk
 13775-13780  _scraper_session
 26523-26562  _screen_full
 12802-12839  _sec_headers
  2175-2177   _select_stream_from_data_section
 28444-28628  _selfcheck
  8697-8731   _send_live_notice
  1213-1217   _should_defer_upload
 25288-25323  _shrink_for_discord
 10383-10395  _sicheres_ziel
 27824-27841  _sign_health_check
 27844-27863  _sign_health_loop
  7752-7763   _spawn
  7766-7796   _spawn_from_flask
 22400-22403  _st_befund
 19168-19409  _start_chat_listener
 13738-13755  _start_loop_watchdog
 12462-12490  _stats_loop
 12441-12444  _stats_output_path
 12447-12459  _stats_write
  8425-8441   _storage_cleanup_loop
 27883-27890  _story_for
  3213-3219   _stream_url_expiry
  3228-3234   _stream_url_is_fresh
  3221-3226   _stream_url_ttl
 17311-17318  _streamer_persona_get
 17293-17299  _streamer_personas_load
 17290-17291  _streamer_personas_path
 17301-17309  _streamer_personas_save
 15112-15116  _studio_chain
 24992-25114  _system_backup
 25117-25147  _system_backup_loop
 11411-11450  _test_proxy
 12117-12126  _testpush_cfg
 12129-12146  _testpush_exec
 12098-12114  _testpush_resolve_live
  7899-7920   _tg_sprache_setzen
  8604-8614   _tg_topics_load_into_mem
  8601-8602   _tg_topics_path
  8616-8623   _tg_topics_save
 10191-10199  _token_ok
  8626-8630   _topic_forget
 14186-14197  _tracking_max_duration
  4198-4212   _tracking_remove_cleanup
  4229-4241   _tracking_resume_cleanup
  1447-1470   _try_attach_file_handler
 21339-21347  _tts_cleanup
 12054-12058  _tunnel_effective
 20802-20855  _twitch_channel_status
 26565-26710  _twitch_chat_loop
 26379-26482  _twitch_eventsub_loop
  1236-1249   _upload_queue_add
  1260-1262   _upload_queue_count
  1219-1228   _upload_queue_load
  1209-1211   _upload_queue_path
  1251-1258   _upload_queue_remove
  1230-1234   _upload_queue_save
  1264-1305   _upload_window_loop
  7616-7623   _uptime_s
 14619-14628  _url_host
   717-734    _url_ohne_zugang
   802-806    _usage_record_claude
  7837-7881   _verbindung_verloren
  6746-6777   _viewer_sample_loop
  6793-6800   _viewer_stats
 10280-10283  _wants_html
  7626-7640   _warn_empty_env
 27613-27734  _watchdog_loop
 26118-26126  _wchat_thank_ok
 19002-19032  _whisper_get_model
  7713-7720   _whisper_native_section
 18211-18217  _whisper_pool
 19101-19130  _whisper_segments
 19034-19098  _whisper_transcribe
 14943-15105  _write_restream_overlay
 26738-26818  _youtube_api_chat_loop
 20858-20961  _youtube_api_status
 20964-21031  _youtube_channel_status
 26821-26982  _youtube_chat_loop
 25978-25991  _youtube_restream_autoconfig
 25994-26018  _youtube_restream_autoconfig_inner
 26085-26113  _youtube_send
 21099-21140  _youtube_set_channel
 26021-26055  _yt_access_token
 26058-26073  _yt_live_chat_id
 26731-26735  _yt_oauth_configured
 26081-26082  _yt_sendrate_cfg
 26713-26728  _yt_timeout
  2745-2746   _ytdlp_detect_available
  2748-2759   _ytdlp_note_result
 13625-13627  _zombie_child_count
  7493-7517   about
  4108-4112   add_ai_log_entry
  4025-4028   add_archive_entry
  4724-4739   add_archive_rule
  4400-4434   add_recording
  4173-4190   add_tracking
  6136-6169   ai
  3760-3811   ai_chat
  3845-3855   ai_history_append
  3857-3862   ai_history_clear
  3834-3843   ai_history_load
  3819-3832   ai_rate_limit_check
  6198-6206   aireset
 18542-18561  azrael_chat
 26987-27109  brain_cmd
  3237-3421   build_recording_cmd
  4193-4196   bulk_add_trackings
  6990-7049   bulkadd
  8444-8584   check_all_trackings
  4245-4257   claim_live_transition
 17387-18149  class KickModerator
 15721-17136  class RestreamManager
 11828-11870  classify_proxy_anonymity
  6244-6442   cleanup
  5207-5248   cleanup_old_recordings
  4391-4398   clear_recording
 25730-25795  clip_moment
  4555-4604   compute_storage_forecast
  7112-7156   cookies_cmd
  4164-4170   count_trackings_for_chat
  4095-4106   decide_preferred_recorder
  4035-4038   delete_archive_entry
  4741-4749   delete_archive_rule
  5673-5820   diag
 27221-27282  einnahmen_cmd
  4549-4552   find_recordings_by_fingerprint
  4056-4072   finish_recording_attempt
  4217-4219   get_all_active_trackings
  4123-4126   get_all_checks
  4436-4439   get_all_recordings
  4498-4500   get_all_tags_with_counts
  4526-4529   get_annotations_for_recording
  4030-4033   get_archive_entry
  4519-4522   get_bookmarked_recordings
  1924-2041   get_cookie_health
  4486-4492   get_event_log
  4079-4093   get_last_recording_attempt
  2826-2931   get_live_status
  5007-5010   get_manual_recordings
  4534-4537   get_or_compute_inspect_sync
  5283-5327   get_outcome_breakdown
  4505-4508   get_priority_poll_interval
  4702-4711   get_profile_snapshots
  4074-4077   get_recent_recording_attempts
  4441-4444   get_recording_by_id
  4512-4515   get_recording_note
  3555-3578   get_redis
  4153-4156   get_stats
  5174-5205   get_storage_stats
  4842-4844   get_tiktok_status_distribution
  4259-4268   get_tracking_state
  4214-4215   get_trackings_for_group
  5023-5026   get_trash_recordings
  9352-10015  handle_recording_finished
  3955-3980   init_db
  5097-5151   inspect_stream_url
 21458-21460  is_revenue_platform
  4714-4722   list_archive_rules
  5477-5515   live
  7977-7985   live_check_worker
  3630-3664   llm_chat
  3687-3715   llm_chat_sync
  3672-3684   llm_list_models
  4452-4478   log_event
  1515-1548   log_recording_failure
  7306-7355   logs_cmd
 27931-28434  main
  6172-6195   on_ai_media
  7432-7458   on_ai_reply
  7461-7490   on_azrael_mention
  7522-7552   on_callback
 18564-18668  oracle_handle
  7195-7198   pause_tracking
  5337-5342   profile_keyboard
  7257-7303   quota
  8355-8422   reaper_loop
  4838-4840   record_tiktok_status
  6211-6241   recstatus
  3580-3588   redis_get_json
  3590-3596   redis_set_json
 27285-27295  report_cmd
 11873-11875  report_proxy_result
  2289-2316   resolve_tiktok_live_stream
  5018-5021   restore_recording
  7201-7204   resume_tracking
  4752-4832   run_archive_rules
 27298-27520  run_bot
 13547-13594  run_flask
  4630-4675   sample_bandwidth_for_active
  4681-4700   save_profile_snapshot
  4115-4121   save_tiktok_check
  4383-4389   set_recording_file
  4222-4226   set_tracking_paused
  5013-5016   soft_delete_recording
  8737-9350   split_and_send_video
  5390-5432   start
  4040-4054   start_recording_attempt
  6445-6483   stats
  4988-5005   stop_manual_recording
  7207-7254   stoprec
  6670-6678   summary_cmd
  7358-7429   sysres
  5822-5966   teststream
  5434-5475   tiktok
  7052-7109   topusers
  5552-5609   track
  5517-5549   track_exact
  5623-5671   tracklist
  4854-4986   trigger_manual_recording
  4344-4381   try_acquire_recording_lock
  5029-5088   universal_search
  5611-5621   untrack
 27112-27218  update_cmd
  4544-4547   update_recording_fingerprint
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
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
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
util.py                datei_in
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
